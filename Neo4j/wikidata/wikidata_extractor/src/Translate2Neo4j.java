import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

public class Translate2Neo4j {
	WikidataReader wr = new WikidataReader ();
	public static String outputFolder = "../data/wikidata2graphModeling/";
	public static String inputFolder = "../data/input/";
	public static float ratio_rand_negative_polarity = 0.05f;
	public static boolean lowWeight = true;
	public static boolean weightsNormalization = false;

	public Translate2Neo4j(String file) {
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
				if(w.proba > 0 || !weightsNormalization) {
					//weights normalization
					if(weightsNormalization) {
						w.proba = w.proba % 10;
						w.proba /= 10.0;
					}
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
			if(ratio_rand_negative_polarity > 0) {
				int rand;
				while (nb_rand_negative_polarity > 0) {
					rand = new Double(Math.floor(Math.random()*lines.size())).intValue();
					Wikiline l = lines.get(rand);
					if(l.polarity && (!lowWeight || l.proba < sum_true/nb_true)) {
						l.polarity = false;
						nb_rand_negative_polarity--;
						System.out.println("nb rand remaining: "+nb_rand_negative_polarity);
					}
				}
			}
			System.out.println(file+"\tproba ("+ratio_rand_negative_polarity+") | valid "+min_true+"-"+max_true+", nb:"+nb_true+", avg:"+(sum_true/nb_true)+"| invalid "+min_false+"-"+max_false+", nb:"+nb_false+", avg:"+(sum_false/nb_false));
			writeCSV (lines, file);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (Exception e) {
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
		zipFile(f);
	}

	public static String fileName (int falseFact, int nbFact) {
		return "rockit_wikidata_"+falseFact+"_"+nbFact+"k.csv";
	}
	
	public static void initOutput() throws Exception {
		String subFolder = "pol-"+ratio_rand_negative_polarity+"_normalizedWeights-"+weightsNormalization+"_lowWeights-"+lowWeight;
		File f = new File(outputFolder);
		f.mkdir();

		outputFolder += subFolder + "/";
		f = new File(outputFolder);
		f.mkdir();
	}

	private static List<String> readFolder () {
		List<String> files = new ArrayList<String> ();
		try {
			File f = new File(inputFolder);
			System.out.println(inputFolder);
			File[] listOfFiles = f.listFiles();

			for (File file : listOfFiles) {
			    if (file.isFile()) {
			    	files.add(file.getName());
			    }
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return files;
	}

	private void zipFile (String sourceFile) throws IOException {
		FileOutputStream fos = new FileOutputStream(outputFolder + sourceFile +".zip");
        ZipOutputStream zipOut = new ZipOutputStream(fos);

        File fileToZip = new File(outputFolder + "sameAs_"+sourceFile);
        FileInputStream fis = new FileInputStream(fileToZip);

        ZipEntry zipEntry = new ZipEntry(fileToZip.getName());
        zipOut.putNextEntry(zipEntry);
        byte[] bytes = new byte[1024];
        int length;
        while((length = fis.read(bytes)) >= 0) {
            zipOut.write(bytes, 0, length);
        }

        fis.close();
        fileToZip.delete();
        fis = null;
        fileToZip = null;

        fileToZip = new File(outputFolder + "pinstConf_"+sourceFile);
        fis = new FileInputStream(fileToZip);

        zipEntry = new ZipEntry(fileToZip.getName());
        zipOut.putNextEntry(zipEntry);
        while((length = fis.read(bytes)) >= 0) {
            zipOut.write(bytes, 0, length);
        }

        fis.close();
        fileToZip.delete();
        fis = null;
        fileToZip = null;

        zipOut.close();
        fos.close();
	}

	public static void main (String args []) {
		boolean set = true;
		if(args.length > 0) {
			try {
				for(String s : args) {
					if(s.startsWith("--input=")) {
						inputFolder = s.substring(8);
					} else if(s.startsWith("--output=")) {
						outputFolder = s.substring(9);
					} else if(s.startsWith("--ratio=")) {
						ratio_rand_negative_polarity = new Float(s.substring(8));
					} else if(s.startsWith("--lowWeight=")) {
						lowWeight = s.substring(13).compareTo("true") == 0;
					} else
						set = false;
				}
			} catch (Exception e) {
				set = false;
			}
		}
		
		
		if(!set){
			System.out.println("The rockit extractor must specify the input and output folders:\n"
					+ "java -jar Translate2Neo4j --input="+inputFolder+" --output="+outputFolder+"\n"
					+ "But also if output evidences could have polarities (ratio and low weighted polarities)\n"
					+ "\t--ratio="+ratio_rand_negative_polarity
					+ "\t--lowWeight="+lowWeight);
		} else {
			System.out.println("Rockit extractor with params:\n"
					+ "\tinputFolder="+inputFolder+"\n"
					+ "\toutputFolder="+outputFolder+"\n"
					+ "\tpolarities ratio="+ratio_rand_negative_polarity+", and low weighted polarities lowWeight="+lowWeight);
		}

		try {
			initOutput ();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		for(String file : readFolder()) {
			new Translate2Neo4j(file);
		}
		/*
		
		new Translate2Neo4j(fileName(1,5), ratio_rand_negative_polarity, lowWeight);
		new Translate2Neo4j(fileName(0,250), ratio_rand_negative_polarity, lowWeight);
		new Translate2Neo4j(fileName(100,250), ratio_rand_negative_polarity, lowWeight);
		*/
	}
}
