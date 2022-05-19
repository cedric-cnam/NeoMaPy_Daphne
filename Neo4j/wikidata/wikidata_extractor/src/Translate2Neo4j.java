import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class Translate2Neo4j {
	WikidataReader wr = new WikidataReader ();
	String outputFolder = "data/output/";
	
	public Translate2Neo4j(String file, float ratio_rand_negative_polarity, boolean lowWeight) {
		try {
			List<Wikiline> lines = wr.readFile (file);
			int nb_rand_negative_polarity = new Float(new Float(lines.size()).floatValue()*ratio_rand_negative_polarity).intValue();
			float min_true = 1.0f;
			float max_true = 0;
			float min_false = 1.0f;
			float max_false = 0;
			float sum_true = 0;
			float nb_true = 0;
			float sum_false = 0;
			float nb_false = 0;
			for(Wikiline w : lines) {
				if(w.proba > 0) {
					//weights normalization
					w.proba = w.proba % 10;
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
			int rand;
			while (nb_rand_negative_polarity > 0) {
				rand = new Double(Math.floor(Math.random()*lines.size())).intValue();
				Wikiline l = lines.get(rand);
				if(l.polarity && (!lowWeight || l.proba < sum_true/nb_true)) {
					l.polarity = false;
					nb_rand_negative_polarity--;
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
		sameAs_bw.write("type;ID_TF;ID_s;ID_p\n");
		BufferedWriter p_bw = new BufferedWriter (new FileWriter (outputFolder +"pinstConf_"+f));
		p_bw.write("type;ID_TF;ID_s;ID_o;ID_p;date_start;date_end;valid;proba;polarity\n");
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

	public static String fileName (int falseFact, int nbFact) {
		return "rockit_wikidata_"+falseFact+"_"+nbFact+"k.csv";
	}
	
	public static void main (String args []) {
		float ratio_rand_negative_polarity = 0.1f;
		boolean lowWeight = true;
		

		new Translate2Neo4j(fileName(0,5), ratio_rand_negative_polarity, lowWeight);
		new Translate2Neo4j(fileName(1,5), ratio_rand_negative_polarity, lowWeight);
		new Translate2Neo4j(fileName(0,250), ratio_rand_negative_polarity, lowWeight);
		new Translate2Neo4j(fileName(100,250), ratio_rand_negative_polarity, lowWeight);
	}
}
