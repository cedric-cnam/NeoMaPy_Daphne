package neoMaPy;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import neoMaPy.connection.Connection;
import neoMaPy.ui.GraphStream;

public class NeoMaPy {
	private Connection connection;

	private GraphStream gs = null;
	public static String inputFile = null;

	private static JSONParser parser = null;
	public static JSONObject config;

	public NeoMaPy() throws Exception {
		init();
	}

	public void init() throws Exception {
		config = readJSONFile("conf/config.json");
		connection = new Connection();
		gs = new GraphStream();
	}

	public void close() throws Exception {
		connection.close();
	}

	private void resultQueries(String fileQueries) {
		System.out.println("----------------");
		List<Query> queries = readQueries((String) config.get("queriesFolder") + fileQueries);
		connection.loadGraph(queries, gs.getGraph());
		gs.doLayout();
		gs.viewer();
	}

	public void viewer() {
		// gs.viewer();
	}

	private List<Query> readQueries(String queryFile) {
		System.out.println(queryFile);
		List<Query> queries = new ArrayList<Query>();

		try {
			BufferedReader br = new BufferedReader(new FileReader(queryFile));
			String line;
			String instruction = "";
			String query = "";
			while ((line = br.readLine()) != null) {
				if (line.startsWith("//")) {
					instruction = line.substring(2);
				} else if (line.endsWith(";")) {
					if (query.length() > 0)
						query += "\n\t";
					query += line;
					queries.add(new Query(instruction, query));
					query = "";
				} else if (line.length() > 0) {
					if (query.length() > 0)
						query += "\n\t";
					query += line;
				}
			}
			br.close();
		} catch (Exception e) {
			e.printStackTrace();
		}

		return queries;
	}

	public JSONObject readJSONFile(String file) throws Exception {
		if (parser != null)
			parser.reset();
		else
			parser = new JSONParser();
		BufferedReader br = new BufferedReader(new FileReader(file));
		Object obj = parser.parse(br);
		return (JSONObject) obj;
	}

	public static void main(String[] args) {
		System.setProperty("org.graphstream.ui", "swing");
		System.setProperty("org.graphstream.ui.renderer", "org.graphstream.ui.j2dviewer.J2DGraphRenderer");
	    boolean set = true;
		try {
			if (args.length > 0) {
				try {
					for (String s : args) {
						if (s.startsWith("--queryFile=")) {
							inputFile = s.substring(12);
							int slash = inputFile.lastIndexOf("/");
							if (slash > 0)
								inputFile = inputFile.substring(slash + 1);
						}
						if (s.startsWith("--help")) {
							set = false;
						}
					}
				} catch (Exception e) {
					set = false;
				}
			}

			if (!set || inputFile == null) {
				System.out.println(
						"--queryFile=XXX.cypher  -> The query file which gives the extraction of nodes and edges.");
				System.exit(0);
			}
			System.out.println("queryFile=" + inputFile);

			NeoMaPy npm = new NeoMaPy();
			npm.resultQueries(inputFile);
			npm.viewer();
			npm.close();

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
