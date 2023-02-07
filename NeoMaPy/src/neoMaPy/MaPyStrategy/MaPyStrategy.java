/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.MaPyStrategy;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import neoMaPy.NeoMaPy;
import neoMaPy.Query;
import neoMaPy.connection.Connection;
import neoMaPy.ui.graphstream.NeoMaPyGraph;
import neoMaPy.ui.graphstream.info.MAPBar;

public class MaPyStrategy extends MAPStrategy {
	public static final int tCon = 0, pCon = 1, pInc = 2, tInc = 3, minTopK = 50, maxTopK = 1000;
	public static final int minThreshold = 0, maxThreshold = 10;
	private JSONParser parser = null;
	private int cons;
	private double threshold;
	private int topK;
	private Map<String, String> mapping;
	
	private JSONObject solutions;
	
	public MaPyStrategy(int cons, int topK, double threshold, Map<String, String> mapping, MAPBar mapBar) {
		super (mapBar);
		this.mapping = mapping;
		this.cons = cons;
		this.topK = topK;
		this.threshold = threshold;
	}

	public static String tcons (int cons) {
		switch(cons) {
		case pCon:return "pCon";
		case pInc:return "pInc";
		case tInc:return "tInc";
		case tCon:
		default: return "tCon";
		}
	}
	
	@Override
	public List<String> computeStrategy(NeoMaPyGraph graph) {
		this.resetBar();
		this.setBarMax(7);

		List<Query> queries = NeoMaPy.readQueries((String) NeoMaPy.config.get("MaPyQueries")); 
		this.progressBar();
		
		String noConflictQuery = tcons(cons)+"_noConflicts", conflictQuery = tcons(cons)+"_conflicts", inferredNodesQuery = "inferredNodes";
		
		for(Query q : queries) {
			if(q.instruction.compareTo(noConflictQuery) == 0)
				noConflictQuery = q.query;
			else if(q.instruction.compareTo(conflictQuery) == 0)
				conflictQuery = q.query;
			if(q.instruction.compareTo(inferredNodesQuery) == 0)
				inferredNodesQuery = q.query;
		}
		this.progressBar();
		noConflictQuery = noConflictQuery.replaceAll("<<threshold>>", threshold+"");
		conflictQuery = conflictQuery.replaceAll("<<threshold>>", threshold+"");
		inferredNodesQuery = inferredNodesQuery.replaceAll("<<threshold>>", threshold+"");
		
		Connection.readQueries2JSON("noConflicts.json", noConflictQuery);
		this.progressBar();
		Connection.readQueries2JSON("conflicts.json", conflictQuery);
		this.progressBar();
		Connection.readQueries2JSON("inferred.json", inferredNodesQuery);
		this.progressBar();

		//NeoMaPyFrame.error("Call MaPy with extracted nodes and Top-" + topK);

		launchMaPy ();
		this.progressBar();

		List<String> nodeIds = new ArrayList<String> ();
		try {
			readMAP(nodeIds);
			this.progressBar();
			System.out.println(tcons(cons)+", top-"+topK+", w > "+threshold+" -> "+nodeIds.size()+" nodes in the MAP");
		} catch (IOException | ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return nodeIds;
	}

	private void launchMaPy () {
		Process p;
		try{
		    String [] cmd = {"python3", "./mapy/auto_MaPy.py","./output/mapy/conflicts.json","./output/mapy/noConflicts.json", topK+"", ""+threshold, "output/resultsMaPy/"};
		    p = Runtime.getRuntime().exec(cmd); 
		    p.waitFor();
		    p.destroy();
		} catch (Exception e) {e.printStackTrace();}
	}

	private void readMAP (List<String> nodeIds) throws IOException, ParseException{
		String file = "./output/resultsMaPy/solutions_MaPy.txt";
		BufferedReader br = new BufferedReader (new FileReader (file));
		String l;
		while ((l = br.readLine()) != null) {
			nodeIds.add(nodeMapping(l));
		}
		br.close();
	}

	@SuppressWarnings({ "unused", "unchecked" })
	private void readConnectedComponents (List<String> nodeIds) throws IOException, ParseException {
		String file = "./output/resultsMaPy/listOfDico.json";
		BufferedReader br = new BufferedReader (new FileReader (file));
		if (parser != null)
			parser.reset();
		else
			parser = new JSONParser();
		solutions = (JSONObject)parser.parse(br);
		JSONObject s = (JSONObject)((JSONArray)solutions.get("list")).get(0);
		s.keySet().forEach(k -> {
			nodeIds.add(nodeMapping(k.toString()));
		});
	}

	private String nodeMapping (String nodeId) {
		return mapping.get(nodeId);
	}
}
