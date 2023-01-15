package neoMaPy.ui.graphstream;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class ReadCSS {
	private Map<String, CSSClass> classes = new HashMap<String, CSSClass> ();

	public ReadCSS(String cssFile) {
		try {
			BufferedReader r = new BufferedReader (new FileReader (cssFile));
			String l;
			while ((l=r.readLine()) != null) {
				if(l.startsWith("node.") || l.startsWith("edge.")) {
					CSSClass css = new CSSClass ();
					css.name = l.substring(l.indexOf(".")+1);
					css.name = css.name.substring(0, css.name.indexOf("{"));
					if(l.contains("color")) {
						css.color = l.substring(l.indexOf("color:") + 6);
						css.color = css.color.substring(0, css.color.indexOf(";"));
					}
					if(l.contains("hidden"))
						css.visibility = false;
					classes.put(css.name, css);
				}
			}
			r.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

	public String getColor (String cssClass) {
		CSSClass cc = classes.get(cssClass);
		if(cc != null)
			return cc.color;
		else
			return null;
	}

	public boolean getVisibility (String cssClass) {
		CSSClass cc = classes.get(cssClass);
		if(cc != null)
			return cc.visibility;
		else
			return false;
	}

	private class CSSClass {
		String name;
		String color;
		boolean visibility  = true;
	}
}
