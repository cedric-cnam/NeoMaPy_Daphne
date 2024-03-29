/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import neoMaPy.MaPyStrategy.InvalidStrategy;
import neoMaPy.MaPyStrategy.MAPStrategy;
import neoMaPy.MaPyStrategy.MaPyStrategy;
import neoMaPy.MaPyStrategy.RandomStrategy;
import neoMaPy.MaPyStrategy.SortedStrategy;
import neoMaPy.ui.graphstream.NeoMaPyGraph;
import neoMaPy.ui.graphstream.info.MAPBar;

public class MaPy {
	public static final int DEFAULT_STRATEGY = 1;
	public static final int RANDOM_STRATEGY = 2;
	public static final int CONFLICT_INCREASING_STRATEGY = 3;
	public static final int CONFLICT_DECREASING_STRATEGY = 4;
	public static final int WEIGHT_INCREASING_STRATEGY = 5;
	public static final int WEIGHT_DECREASING_STRATEGY = 6;
	public static final int GOAL_STRATEGY = 7;

	private MAPStrategy strategy;
	private List<String> nodes = new ArrayList<String>();

	public MaPy() {
		strategy = null;
	}

	public static MAPStrategy strategy(int strat, MAPBar mapBar) {
		MAPStrategy strategy;
		switch (strat) {
		case MaPy.CONFLICT_INCREASING_STRATEGY:
			strategy = new SortedStrategy(1, true, mapBar);
			break;
		case MaPy.CONFLICT_DECREASING_STRATEGY:
			strategy = new SortedStrategy(1, false, mapBar);
			break;
		case MaPy.WEIGHT_INCREASING_STRATEGY:
			strategy = new SortedStrategy(2, true, mapBar);
			break;
		case MaPy.WEIGHT_DECREASING_STRATEGY:
			strategy = new SortedStrategy(2, false, mapBar);
			break;
		case MaPy.RANDOM_STRATEGY:
			strategy = new RandomStrategy(mapBar);
			break;
		case MaPy.GOAL_STRATEGY:
			strategy = new InvalidStrategy(mapBar);
			break;
		default:
			strategy = new SortedStrategy(1, false, mapBar);
			break;
		}
		return strategy;
	}

	public static MAPStrategy strategy(int cons, int topK, double threshold, Map<String, String> mapping,
			MAPBar mapBar) {
		return new MaPyStrategy(cons, topK, threshold, mapping, mapBar);
	}

	public boolean processMAP(NeoMaPyGraph graph, MAPStrategy s) {
		if (graph == null || s == null)
			return false;
		strategy = s;
		resetNodes(graph);
		nodes = strategy.computeStrategy(graph);
		removeNodes(graph);
		return true;
	}

	public void resetStrategy() {
		strategy = null;
	}

	public void resetNodes(NeoMaPyGraph graph) {
		graph.nodes().forEach(n -> {
			Boolean b = (Boolean) n.getAttribute("removed");
			if (b != null && b) {
				n.removeAttribute("removed");
				n.removeAttribute("ui.hide");
				n.edges().forEach(e -> {
					e.removeAttribute("ui.hide");
					e.removeAttribute("removed");
				});
			}
		});
	}

	private void removeNodes(NeoMaPyGraph graph) {
		Map<String, Boolean> validNodes = new HashMap<String, Boolean>();
		nodes.forEach(s -> {
			validNodes.put(s, true);
		});
		graph.nodes().forEach(n -> {
			Boolean b = true;
			String type = (String) n.getAttribute("type");
			if (type.compareTo("o") == 0 || type.compareTo("s") == 0 || type.compareTo("p") == 0)
				b = false;

			if (!b)
				return;
			b = validNodes.get(n.getId());
			if (b == null || !b) {
				n.setAttribute("removed", true);
				n.setAttribute("ui.hide");
				n.edges().forEach(e -> {
					e.setAttribute("ui.hide");
				});
			}
		});
	}

	public List<String> getMAPnodes() {
		return nodes;
	}

}
