package pvt.unitee.testobject.lib.java.loader;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import arjunasdk.sysauto.batteries.DataBatteries;
import arjunasdk.sysauto.batteries.FileSystemBatteries;
import pvt.arjunasdk.enums.BatteriesPropertyType;
import pvt.batteries.config.Batteries;
import unitee.annotations.FileDataReference;
import unitee.annotations.Instances;
import unitee.annotations.TestClass;
import unitee.annotations.TestMethod;

public class JavaTestLoadingUtils {
	private static String[] checkArray = new String[] {"NOT_SET"};
	
	private static String getDataRefPath(FileDataReference dataRefAnn) throws Exception{
		String refPath = null;

		if (dataRefAnn.path().equals("NOT_SET")){
			if (dataRefAnn.value().equals("NOT_SET")){
				throw new Exception("Used @FileDataReference annotation by providing neither path nor value attribute.");
			} else {
				refPath = dataRefAnn.value();
			}
		} else {
			refPath = dataRefAnn.path();
		}

		if (!FileSystemBatteries.isFile(refPath)){
			String relRefPath = Batteries.value(BatteriesPropertyType.DIRECTORY_PROJECT_DATA_REFERENCES).asString() + "/" + refPath;
			if (!FileSystemBatteries.isFile(relRefPath)){
				throw new Exception(String.format("File path provided using @FileDataReference annotation is present neither as Arjuna path: %s nor as absolute path: %s:", relRefPath, refPath));
			}
			refPath = relRefPath;
		}		
		
		return refPath;
	}

	public static String getDataRefPath(Class<?> klass) throws Exception{
		return getDataRefPath((FileDataReference) klass.getAnnotation(FileDataReference.class));
	}
	
	public static String getDataRefName(Class<?> klass) throws Exception{
		FileDataReference dataRefAnn = (FileDataReference) klass.getAnnotation(FileDataReference.class); 
		return dataRefAnn.name();
	}
	
	public static int getInstanceThreadCount(Instances ann) throws Exception{
		if (ann.instanceThreads() < 1){
			return -1;
		} else {
			return ann.instanceThreads();
		}
	}
	
	public static int getCreatorThreadCount(Class<?> klass) throws Exception{
		TestClass testClassAnn = (TestClass) klass.getAnnotation(TestClass.class); 
		if (testClassAnn != null){
			return testClassAnn.methodThreads();
		} else {
			return 1;
		}
	}
	
	public static int getTestThreadCount(Method m) throws Exception{
		TestMethod testMethodAnn = (TestMethod) m.getAnnotation(TestMethod.class);
		// DDT methods may not have TestMethod annotation, but are considered as Test Methods.
		if (testMethodAnn != null){
			return testMethodAnn.testThreads();
		} else {
			return 1;
		}
	}
	
	public static String getDataRefName(Method m) {
		FileDataReference dataRefAnn = (FileDataReference) m.getAnnotation(FileDataReference.class); 
		return dataRefAnn.name();
	}
	
	public static String getDataRefPath(Method m) throws Exception{
		return getDataRefPath((FileDataReference) m.getAnnotation(FileDataReference.class));
	}
	
	public static boolean isDataRefPresent(Class<?> klass){
		return klass.isAnnotationPresent(FileDataReference.class);
	}
	
	public static boolean isDataRefPresent(Method m){
		return m.isAnnotationPresent(FileDataReference.class);
	}
	
	public static boolean isInstancesAnnotationPresent(Class<?> klass){
		return klass.isAnnotationPresent(Instances.class);
	}
	
	public static boolean isInstancesAnnotationPresent(Method m){
		return m.isAnnotationPresent(Instances.class);
	}
	
	public static int getInstancesCount(Instances instancesAnnotation){
		int cloneCount = 1;
		if (instancesAnnotation.count() != 1){
			if (instancesAnnotation.count() < 1){
				cloneCount = -1;
			} else {
				cloneCount = instancesAnnotation.count();
			}
		} else {
			if (instancesAnnotation.value() < 1){
				cloneCount = -1;
			} else {
				cloneCount = instancesAnnotation.value();
			}
		}
		return cloneCount;
	}
	
	public static boolean hasUserSuppliedProperties(String mQualifiedName, Instances instancesAnn){
		String[] properties = instancesAnn.execVars();
		if (!Arrays.equals(properties,checkArray)){
			if (properties.length == 0){
				System.err.println("Found empty properties in @Instances annotation: " + mQualifiedName);
				System.err.println("Exiting...");
				System.exit(1);
				return false;
			} else {
				return true;
			}
		} else {
			return false;
		}		
	}
	
	public static Map<Integer,HashMap<String,String>> loadExecVarsFromInstancesAnnotation(Instances instancesAnnotation, int instanceCount, boolean userHasSuppliedProperties){
		Map<Integer,HashMap<String,String>> invocationWiseProps = new HashMap<Integer,HashMap<String,String>>();
		for (int i=1; i <= instanceCount; i++){
			invocationWiseProps.put(i, new HashMap<String,String>());
		}
		
		if (!userHasSuppliedProperties){
			return invocationWiseProps;
		}

		String[] properties = instancesAnnotation.execVars();
		
		for(String propString: properties){
			List<String> parts = DataBatteries.split(propString,"=");
			String propKey = parts.get(0);
			String propValuesString = parts.get(1);
			for (int i=1; i <= instanceCount; i++){
				invocationWiseProps.get(i).put(propKey, null);
			}
			
			// We need to be careful here. Instance count is human count, starts with 1.
			// Prop Values is computer counting, starts from 0
			List<String> propValues = DataBatteries.split(propValuesString,",");
			String lastValue = null;
			for (int i=1; i <= instanceCount; i++){
				if (i <= propValues.size()){
					lastValue = propValues.get(i-1);
				}
				invocationWiseProps.get(i).put(propKey, lastValue);
			}
		}
		return invocationWiseProps;
	}

}