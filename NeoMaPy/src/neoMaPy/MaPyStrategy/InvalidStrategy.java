/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.MaPyStrategy;

import java.util.ArrayList;
import java.util.List;

import neoMaPy.ui.graphstream.NeoMaPyGraph;

public class InvalidStrategy extends MAPStrategy {

	public InvalidStrategy() {
		// TODO Auto-generated constructor stub
	}

	@Override
	public List<String> computeStrategy(NeoMaPyGraph graph) {
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
