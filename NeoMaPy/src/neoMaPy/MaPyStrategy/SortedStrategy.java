/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.MaPyStrategy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Stream;

import org.graphstream.graph.Node;

import neoMaPy.ui.graphstream.NeoMaPyGraph;

public class SortedStrategy extends MAPStrategy {
	private int type;
	private boolean increasing;
	public SortedStrategy(int type, boolean increasing) {
		this.type = type;
		this.increasing = increasing;
	}

	@Override
	public List<String> computeStrategy(NeoMaPyGraph graph) {
		Map<String, Long> conflictNodes = new HashMap<String, Long>();
		graph.nodes().forEach(n -> {
			if(((String)n.getAttribute("type")).compareTo("TF") == 0) {
				long l;
				if(type == 1)
					l = n.edges().count();
				else {
					l = new Double (((Double)n.getAttribute("weight"))*1000.0).longValue();
				}
				conflictNodes.put(n.getId(), l);
			}
		});
		List<String> nodes = new ArrayList<String>();

		Stream<Map.Entry<String,Long>> sorted;
		if(increasing)
			sorted = conflictNodes.entrySet().stream()
		       .sorted(Map.Entry.comparingByValue());
		else
			sorted = conflictNodes.entrySet().stream()
				.sorted(Collections.reverseOrder(Map.Entry.comparingByValue()));
		
		sorted.forEach( entry ->{
			String key = entry.getKey();
			Node n = graph.getNode(key);
			AtomicInteger nb = new AtomicInteger(0);
			n.edges().forEach(e -> {
				e.attributeKeys().forEach( k -> {
					if(k.compareTo("o") == 0 || k.compareTo("s") == 0 || k.compareTo("p") == 0 || k.compareTo("ui.class") == 0)
						return;
					else {
						Boolean b = (Boolean) e.getAttribute("removed");
						if (b == null || !b) {
							nb.addAndGet(1);
							return;
						}
					}
				});
			});
			if(nb.get() > 0) {
				n.setAttribute("removed", true);
				n.edges().forEach(e -> {
					e.setAttribute("removed", true);
				});
			} else 
				nodes.add(n.getId());
		});
		return nodes;
	}

}
