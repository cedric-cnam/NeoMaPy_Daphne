package neoMaPy.MaPyStrategy;

import java.util.ArrayList;
import java.util.List;

import neoMaPy.ui.graphstream.NeoMaPyGraph;

public class MaPyStrategy extends Strategy {
	private int cons;
	private int topK;

	public MaPyStrategy(int cons, int topK) {
		this.cons = cons;
		this.topK = topK;
	}

	@Override
	public List<String> strategy(NeoMaPyGraph graph) {
		System.out.println("Call Python with cons(" + cons + ") & top-" + topK);
		System.out.println("Take output (nodes to keep)");
		List<String> nodes = new ArrayList<String>();
		graph.nodes().forEach(n -> {
			nodes.add(n.getId());
		});
		System.out.println(nodes.size() + " nodes in the MAP");
		return nodes;
	}

}
