/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.MaPyStrategy;

import java.util.ArrayList;
import java.util.List;

import neoMaPy.ui.graphstream.NeoMaPyGraph;

public class RandomStrategy extends MAPStrategy {

	public RandomStrategy() {
		
	}

	public List<String> computeStrategy(NeoMaPyGraph graph) {
		List<String> nodes = new ArrayList<String>();
		graph.nodes().forEach(n -> {
			if (Math.random() > 0.25d) {
				nodes.add(n.getId());
			}
		});
		return nodes;
	}

}
