/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy.ui.graphstream;

import java.awt.event.MouseEvent;
import java.util.EnumSet;

import org.graphstream.ui.graphicGraph.GraphicElement;
import org.graphstream.ui.swing_viewer.util.DefaultMouseManager;
import org.graphstream.ui.view.util.InteractiveElement;

public class NeoMaPyMouseManager extends DefaultMouseManager {
	GraphStreamPanel gs;

	NeoMaPyMouseManager(GraphStreamPanel gs) {
		super();
		this.gs = gs;
	}

	@Override
	public void mouseMoved(MouseEvent event) {
		/*
		 * try { GraphicElement ge =
		 * view.findGraphicElementAt(EnumSet.of(InteractiveElement.NODE,
		 * InteractiveElement.EDGE), event.getX(), event.getY()); if (ge != null)
		 * gs.setInfo(ge); } catch (Exception e) {
		 * 
		 * }
		 */
	}

	@Override
	public void mouseClicked(MouseEvent event) {
		try {
			GraphicElement ge = view.findGraphicElementAt(EnumSet.of(InteractiveElement.NODE), event.getX(),
					event.getY());
			if (ge != null)
				gs.setInfo(ge.getId());
		} catch (Exception e) {

		}

	}
}
