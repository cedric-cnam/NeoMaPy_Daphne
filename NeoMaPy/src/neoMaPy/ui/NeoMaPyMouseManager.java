package neoMaPy.ui;

import java.awt.event.MouseEvent;
import java.util.EnumSet;

import org.graphstream.ui.graphicGraph.GraphicElement;
import org.graphstream.ui.swing_viewer.util.DefaultMouseManager;
import org.graphstream.ui.view.util.InteractiveElement;

public class NeoMaPyMouseManager extends DefaultMouseManager {
	GraphStream gs;

	NeoMaPyMouseManager(GraphStream gs) {
		super();
		this.gs = gs;
	}

	public void mouseMoved(MouseEvent event) {
/*		try {
			GraphicElement ge = view.findGraphicElementAt(EnumSet.of(InteractiveElement.NODE, InteractiveElement.EDGE),
					event.getX(), event.getY());
			if (ge != null)
				gs.setInfo(ge);
		} catch (Exception e) {

		}
*/
	}

	public void mouseClicked(MouseEvent event) {
		try {
			GraphicElement ge = view.findGraphicElementAt(EnumSet.of(InteractiveElement.NODE),
					event.getX(), event.getY());
			if (ge != null)
				gs.setInfo(ge.getId());
		} catch (Exception e) {

		}

	}
}
