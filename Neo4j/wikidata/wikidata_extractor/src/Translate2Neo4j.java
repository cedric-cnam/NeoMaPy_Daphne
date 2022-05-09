import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class Translate2Neo4j {
	WikidataReader wr = new WikidataReader ();
	String outputFolder = "data/output/";
	
	public Translate2Neo4j(String file) {
		try {
			List<Wikiline> lines = wr.readFile (file);
			float min_true = lines.get(0).proba;
			float max_true = 0;
			float min_false = lines.get(0).proba;
			float max_false = 0;
			float sum_true = 0;
			float nb_true = 0;
			float sum_false = 0;
			float nb_false = 0;
			for(Wikiline w : lines) {
				if(w.proba > 0) {
					w.proba /= 10.0;
					if(w.valid) {
						min_true = Math.min(min_true, w.proba);
						max_true = Math.max(max_true, w.proba);
						sum_true += w.proba;
						nb_true++;
					} else {
						min_false = Math.min(min_false, w.proba);
						max_false = Math.max(max_false, w.proba);
						sum_false += w.proba;
						nb_false++;
					}
				}
			}
			System.out.println("proba | true "+min_true+"-"+max_true+", nb:"+nb_true+", avg:"+(sum_true/nb_true)+"| false "+min_false+"-"+max_false+", nb:"+nb_false+", avg:"+(sum_false/nb_false));
			writeCSV (lines, file);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void writeCSV (List<Wikiline> lines, String f) throws IOException {
		BufferedWriter sameAs_bw = new BufferedWriter (new FileWriter (outputFolder + "sameAs_"+f));
		sameAs_bw.write("type;ID_TF;ID_from;ID_to\n");
		BufferedWriter p_bw = new BufferedWriter (new FileWriter (outputFolder +"pinstConf_"+f));
		p_bw.write("type;ID_TF;ID_from;ID_to;ID_o;date_start;date_end;valid;proba\n");
		for(Wikiline w : lines) {
			if(w.type.compareTo("sameAs")==0) {
				sameAs_bw.write(w.toString());
				sameAs_bw.write("\n");
			} else {
				p_bw.write(w.toString());
				p_bw.write("\n");
			}
			
		}
		sameAs_bw.flush();
		sameAs_bw.close();
		p_bw.flush();
		p_bw.close();
	}
	
	public static void main (String args []) {
		String file = "rockit_wikidata_0_5k.csv";
		new Translate2Neo4j(file);
		file = "rockit_wikidata_1_5k.csv";
		new Translate2Neo4j(file);
	}
}
