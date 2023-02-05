/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.MaPyStrategy;

import java.util.List;

import neoMaPy.ui.graphstream.NeoMaPyGraph;

public abstract class MAPStrategy {

	public MAPStrategy() {
		
	}

	public abstract List<String> computeStrategy(NeoMaPyGraph graph); 
}
