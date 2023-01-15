package neoMaPy;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import neoMaPy.connection.Connection;
import neoMaPy.ui.NeoMaPyFrame;

public class NeoMaPy {
	private static Connection connection;

	private static NeoMaPyFrame nmp = null;
	public static String inputFile = null;

	private static JSONParser parser = null;
	public static JSONObject config;

	public NeoMaPy() throws Exception {
		init();
	}

	public void init() throws Exception {
		config = readJSONFile("conf/config.json");
		connection = new Connection();
		nmp = new NeoMaPyFrame();
		nmp.init();
	}

	public static boolean connection () {
		return connection.connect();
	}
	
	public void close() throws Exception {
		connection.close();
	}

	public static void loadGraph() {
		List<Query> queries = readQueries((String) config.get("extractGraphQueries"));
		connection.loadGraph(queries, nmp.getGraph());
	}

	public void viewer() {
		// gs.viewer();
	}

	public static Map<String, Integer> statQueries (){
		Map<String, Integer> stats = Connection.loadStats(readQueries((String)NeoMaPy.config.get("statsQueries")));
		return stats;
	}
	
	public static List<Query> readQueries(String queryFile) {
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
						query += "\n";
					query += line;
					queries.add(new Query(instruction, query));
					query = "";
				} else if (line.length() > 0) {
					if (query.length() > 0)
						query += "\n";
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
		try {
			new NeoMaPy();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
