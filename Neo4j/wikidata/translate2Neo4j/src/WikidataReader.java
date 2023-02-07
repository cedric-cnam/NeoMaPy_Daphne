/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class WikidataReader {
	BufferedReader br;
	public WikidataReader() {
	}

	public List<Wikiline> readFile (String f) throws IOException {
		List<Wikiline> lines = new ArrayList<Wikiline> ();
		br = new BufferedReader (new FileReader (Translate2Neo4j.inputFolder +f));
		String line;
		String [] l;
		while( (line = br.readLine()) != null) {
			try{
				Wikiline w = new Wikiline ();
				l = line.split(",");
				w.type = l[0].substring(0, l[0].indexOf("("));
				w.ID_s = w.extractString(l[0]);
				if(w.type.compareTo("pinstConf") == 0) {
					w.ID_o = w.extractString(l[2]);
					w.ID_p = w.extractString(l[1]);
					w.date_start = w.extractDate(l[3]);
					w.date_end = w.extractDate(l[4]);
					if(w.extractString(l[5]).compareTo("true") == 0)
						w.valid = true;
					w.proba = w.extractFloat(l[6]);
					
				} else {
					w.ID_p = w.extractString(l[1]);
				}
				lines.add(w);
			} catch (Exception e) {System.out.println(line);e.printStackTrace();}
		}
		System.out.println("Nb lines: "+lines.size());
		return lines;
	}
}
