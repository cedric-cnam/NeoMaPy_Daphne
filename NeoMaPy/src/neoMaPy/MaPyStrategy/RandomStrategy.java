/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.MaPyStrategy;

import java.util.ArrayList;
import java.util.List;

import neoMaPy.ui.graphstream.NeoMaPyGraph;
import neoMaPy.ui.graphstream.info.MAPBar;

public class RandomStrategy extends MAPStrategy {

	public RandomStrategy(MAPBar mapBar) {
		super(mapBar);
	}

	@Override
	public List<String> computeStrategy(NeoMaPyGraph graph) {
		this.resetBar();
		this.setBarMax(new Long(graph.nodes().count()).intValue());
		List<String> nodes = new ArrayList<String>();
		graph.nodes().forEach(n -> {
			if (Math.random() > 0.25d) {
				nodes.add(n.getId());
			}
			this.progressBar();
		});
		return nodes;
	}
}
