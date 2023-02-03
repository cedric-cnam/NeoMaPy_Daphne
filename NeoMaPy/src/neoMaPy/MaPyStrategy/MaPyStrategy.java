package neoMaPy.MaPyStrategy;

import java.util.ArrayList;
import java.util.List;

import neoMaPy.NeoMaPy;
import neoMaPy.Query;
import neoMaPy.connection.Connection;
import neoMaPy.ui.NeoMaPyFrame;
import neoMaPy.ui.graphstream.NeoMaPyGraph;

public class MaPyStrategy extends Strategy {
	public static final int tCon = 0, pCon = 1, pInc = 2, tInc = 3, minTopK = 50, maxTopK = 1000;
	public static final int minThreshold = 0, maxThreshold = 10;
	private int cons;
	private double threshold;
	private int topK;
	

	public MaPyStrategy(int cons, int topK, double threshold) {
		this.cons = cons;
		this.topK = topK;
		this.threshold = threshold;
	}

	private String tcons (int cons) {
		switch(cons) {
		case pCon:return "pCon";
		case pInc:return "tInc";
		case tInc:return "tInc";
		case tCon:
		default: return "tCon";
		}
	}
	
	@Override
	public List<String> strategy(NeoMaPyGraph graph) {
		NeoMaPyFrame.error("Extract nodes for the MAP Inference with: "
				+ "cons(" + tcons(cons) + "), threshold-"+threshold);
		List<Query> queries = NeoMaPy.readQueries((String) NeoMaPy.config.get("MaPyQueries")); 
		
		String noConflictQuery = tcons(cons)+"_noConflicts", conflictQuery = tcons(cons)+"_conflicts", inferredNodesQuery = "inferredNodes";
		
		for(Query q : queries) {
			if(q.instruction.compareTo(noConflictQuery) == 0)
				noConflictQuery = q.query;
			else if(q.instruction.compareTo(conflictQuery) == 0)
				conflictQuery = q.query;
			if(q.instruction.compareTo(inferredNodesQuery) == 0)
				inferredNodesQuery = q.query;
		}
		noConflictQuery = noConflictQuery.replaceAll("<<threshold>>", threshold+"");
		conflictQuery = conflictQuery.replaceAll("<<threshold>>", threshold+"");
		inferredNodesQuery = inferredNodesQuery.replaceAll("<<threshold>>", threshold+"");
		
		Connection.readQueries2JSON("noConflicts.json", noConflictQuery);
		Connection.readQueries2JSON("conflicts.json", conflictQuery);
		Connection.readQueries2JSON("inferred.json", inferredNodesQuery);

		NeoMaPyFrame.error("Call MaPy with extracted nodes and Top-" + topK);

		
		System.out.println("Take output (nodes to keep)");
		List<String> nodes = new ArrayList<String>();
		graph.nodes().forEach(n -> {
			nodes.add(n.getId());
		});
		System.out.println(nodes.size() + " nodes in the MAP");
		return nodes;
	}

}
