/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.MaPyStrategy;

import java.util.List;

import neoMaPy.ui.graphstream.NeoMaPyGraph;
import neoMaPy.ui.graphstream.info.MAPBar;

public abstract class MAPStrategy {
	protected MAPBar mapBar;

	public MAPStrategy(MAPBar mapBar) {
		this.mapBar = mapBar;
	}

	protected void setBarMax(int value) {
		mapBar.setBarMax(value);
	}

	protected void progressBar() {
		mapBar.changeStatus();
	}

	protected void resetBar() {
		mapBar.resetStatus();
	}

	public abstract List<String> computeStrategy(NeoMaPyGraph graph);
}
