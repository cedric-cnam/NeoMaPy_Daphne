import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import org.json.simple.JSONObject;
import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Config;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Record;
import org.neo4j.driver.Result;
import org.neo4j.driver.Session;
import org.neo4j.driver.Transaction;
import org.neo4j.driver.TransactionWork;

public class Connection implements AutoCloseable {
	private final Driver driver;
	private BufferedWriter log;

	private String outputFolder;

	public Connection() throws Exception {
		Config config = Config.builder().build();
		driver = GraphDatabase.driver((String) GraphModeling.config.get("URI"),
				AuthTokens.basic((String) GraphModeling.config.get("user"), (String) GraphModeling.config.get("mdp")),
				config);
	}

	@Override
	public void close() throws Exception {
		driver.close();
		log.flush();
		log.close();
	}

	public void initLog(String file, String subFolder) throws Exception {
		outputFolder = "output/" + file + "/";
		File f = new File(outputFolder);
		f.mkdir();
		outputFolder = "output/" + file + "/"+subFolder+"/";
		f = new File(outputFolder);
		f.mkdir();
		log = new BufferedWriter(new FileWriter(outputFolder + "time.csv"));
		log.write("STEP;QUERY;TIME (ms)\n");
	}

	public void log(String step, String query, long time) throws IOException {
		System.out.println(step + "\t" + query + "\t" + time + " ms");
		log.write(step + ";" + query + ";" + time);
		log.newLine();
		if (query.compareTo("TOTAL") == 0)
			log.newLine();
	}

	public void updateQueries(String step, List<Query> queries) {
		long total = 0l;
		Instant start, end;
		Duration timeElapsed;
		for (Query q : queries) {
			try (Session session = driver.session()) {
				start = Instant.now();
				session.run(q.query);
				end = Instant.now();
				timeElapsed = Duration.between(start, end);
				total += timeElapsed.toMillis();
				try {
					log(step, q.instruction, timeElapsed.toMillis());
				} catch (IOException e) {
					e.printStackTrace();
				}
			} catch (org.neo4j.driver.exceptions.ServiceUnavailableException e) {
				e.printStackTrace();
				System.exit(0);
			} catch (Exception e) {
				e.printStackTrace();
			}
		} 
		try {
			log(step, "TOTAL", total);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void readQueries2CSV(String step, List<Query> queries, String csvFile) {
		try (Session session = driver.session()) {
			session.readTransaction(new TransactionWork<Integer>() {
				@Override
				public Integer execute(Transaction tx) {
					Instant start, end;
					Duration timeElapsed;
					BufferedWriter output = null;
					try {
						output = new BufferedWriter(new FileWriter(outputFolder + csvFile+".csv"));
						for (Query q : queries) {
							start = Instant.now();
							Result result = tx.run(q.query);
							end = Instant.now();
							timeElapsed = Duration.between(start, end);
							log(step, q.instruction, timeElapsed.toMillis());
							output.newLine();
							for(String s : result.keys()) {
								output.write(";"+s);
							}
							output.newLine();
							while (result.hasNext()) {
								output.write(q.instruction);
								Record r = result.next();
								for(int i=0;i<r.size();i++) {
									output.write(";"+r.get(i));
								}
								output.newLine();
							}
						}
						if(csvFile != null) {
							output.flush();
							output.close();
						}
					} catch (IOException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
					return 1;
				}
			});
		}
	}

	public void readQueries2JSON(String step, List<Query> queries) {
		try (Session session = driver.session()) {
			session.readTransaction(new TransactionWork<Integer>() {
				@Override
				public Integer execute(Transaction tx) {
					Instant start, end;
					Duration timeElapsed;
					BufferedWriter output = null;
					try {
						for (Query q : queries) {
							start = Instant.now();
							Result result = tx.run(q.query);
							end = Instant.now();
							timeElapsed = Duration.between(start, end);
							log(step, q.instruction, timeElapsed.toMillis());
							
							output = new BufferedWriter(new FileWriter(outputFolder + q.instruction+".json"));
							output.write("[");
							if(result.hasNext()) {
								JSONObject o = toJSON(result.next());
								output.write(o.toString());
								
								while (result.hasNext()) {
									o = toJSON(result.next());
									output.write(",\n"+o.toJSONString());
								}
							}
							output.write("]");
							output.flush();
							output.close();
							zipFile(outputFolder + q.instruction, ".json");
						}
					} catch (IOException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
					return 1;
				}
			});
		}
	}

	private void zipFile (String sourceFile, String ext) throws IOException {
		FileOutputStream fos = new FileOutputStream(sourceFile+".zip");
        ZipOutputStream zipOut = new ZipOutputStream(fos);
        File fileToZip = new File(sourceFile+ext);
        FileInputStream fis = new FileInputStream(fileToZip);
        ZipEntry zipEntry = new ZipEntry(fileToZip.getName());
        zipOut.putNextEntry(zipEntry);
        byte[] bytes = new byte[1024];
        int length;
        while((length = fis.read(bytes)) >= 0) {
            zipOut.write(bytes, 0, length);
        }
        zipOut.close();
        fis.close();
        fos.close();
        fileToZip.delete();
	}

	@SuppressWarnings("unchecked")
	private JSONObject toJSON (Record r) {
		JSONObject o = new JSONObject ();
		for(String k : r.keys()) {
			o.put(k, r.get(k));
		}

		return o;
	}
}
