package neoMaPy.MaPyStrategy;

import java.util.ArrayList;
import java.util.List;

import neoMaPy.ui.graphstream.NeoMaPyGraph;

public class RandomStrategy extends Strategy {

	public RandomStrategy() {
		
	}

	public List<String> strategy(NeoMaPyGraph graph) {
		List<String> nodes = new ArrayList<String>();
		graph.nodes().forEach(n -> {
			if (Math.random() > 0.25d) {
				nodes.add(n.getId());
			}
		});
		return nodes;
	}

}
