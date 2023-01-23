package neoMaPy.MaPyStrategy;

import java.util.ArrayList;
import java.util.List;

import neoMaPy.ui.graphstream.NeoMaPyGraph;

public class InvalidStrategy extends Strategy {

	public InvalidStrategy() {
		// TODO Auto-generated constructor stub
	}

	@Override
	public List<String> strategy(NeoMaPyGraph graph) {
		List<String> nodes = new ArrayList<String>();
		graph.nodes().forEach(n -> {
			Boolean valid = (Boolean) n.getAttribute("valid");
			if (valid == null || valid) {
				nodes.add(n.getId());
			}
		});
		return nodes;
	}
}
