package neoMaPy.MaPyStrategy;

import java.util.List;

import neoMaPy.ui.graphstream.NeoMaPyGraph;

public abstract class Strategy {

	public Strategy() {
		
	}

	public abstract List<String> strategy(NeoMaPyGraph graph); 
}
