import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class GraphModeling {
	private Connection connection;
	public static String inputFile = null;

	private static JSONParser parser = null;
	public static JSONObject config;
	public static boolean inference = true;
	
	public String [][] replacements = {
	};

	public GraphModeling() throws Exception {
		init ();
	}

	public void init () throws Exception {
		config = readJSONFile("config.json");
		connection = new Connection ();
		connection.initLog(inputFile,(inference?"withInference":"withoutInference"));
	}

	public void close () throws Exception {
		connection.close();
	}

	public void graphSettings() throws Exception {
		graphSetting ("delete.cypher");
		graphSetting ("schema.cypher");
		graphSetting ("graphSetting.cypher");
	}

	public void inference() throws Exception {
		graphSetting ("inference.cypher");		
	}

	public void constraints() throws Exception {
		graphSetting ("constraints.cypher");
	}
	
	private void graphSetting (String fileQueries) {
		System.out.println("----------------");
		List<Query> queries = readQueries ((String)config.get("queriesFolder") + fileQueries);
		for(Query q : queries) {
			if(q.query.contains("<<FILE>>")) {
				q.query = q.query.replace("<<FILE>>",inputFile);
			}
			for(String [] replacement : replacements) {
				if(q.instruction.compareTo(replacement[0]) == 0) {
					q.query = q.query.replace("<<"+replacement[1]+">>",(String)config.get(replacement[2]));
				}	
			}
		}
		connection.updateQueries(fileQueries, queries);
	}
	
	private void statsQueries (String fileQueries, String csvFile) {
		System.out.println("----------------");
		List<Query> queries = readQueries ((String)config.get("queriesFolder") + fileQueries);
		for(Query q : queries) {
			for(String [] replacement : replacements) {
				if(q.instruction.compareTo(replacement[0]) == 0) {
					q.query = q.query.replace("<<"+replacement[1]+">>",(String)config.get(replacement[2]));
				}
			}
		}
		connection.readQueries2CSV(fileQueries, queries, csvFile);
	}

	private void resultQueries (String fileQueries) {
		System.out.println("----------------");
		List<Query> queries = readQueries ((String)config.get("queriesFolder") + fileQueries);
		for(Query q : queries) {
			for(String [] replacement : replacements) {
				if(q.instruction.compareTo(replacement[0]) == 0) {
					q.query = q.query.replace("<<"+replacement[1]+">>",(String)config.get(replacement[2]));
				}	
			}
		}
		connection.readQueries2JSON(fileQueries, queries);
	}

	private List<Query> readQueries (String queryFile){
		List<Query> queries = new ArrayList<Query> ();

		try {
			BufferedReader br = new BufferedReader (new FileReader (queryFile));
			String line;
			String instruction = "";
			String query = "";
			while( (line = br.readLine()) != null) {
				if(line.startsWith("//")) {
					instruction = line.substring(2);
				} else if (line.endsWith(";")) {
					if(query.length() > 0)
						query += "\n\t";
					query += line;
					queries.add(new Query (instruction, query));
					query = "";
				} else if (line.length() > 0){
					if(query.length() > 0)
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
		if(parser != null)
			parser.reset();
		else
			parser = new JSONParser();
		BufferedReader br = new BufferedReader(new FileReader(file));
		Object obj = parser.parse(br);
		return (JSONObject) obj;
	}

	public static void main (String [] args) {
		try {
			boolean set = true;
			boolean noDelete = false;
			if(args.length > 0) {
				try {
					for(String s : args) {
						if(s.startsWith("--inputFile=")) {
							inputFile = s.substring(12);
						} if(s.startsWith("--inference=")) {
								inference = s.substring(12).compareTo("true")==0;
						} else if(s.startsWith("--help")) {
							set = false;
						} else if(s.startsWith("--noDelete")) {
							noDelete = true;
						}
					}
				} catch (Exception e) {
					set = false;
				}
			}
			
			
			if(!set || inputFile == null){
				System.out.println("--inputFile=XXX.csv  -> evidences that have to be imported. Files must be put in the \"import\" neo4j folder of your database. It removes the previous database and create a new one with the input data.\n"
						+ "--noDelete  -> apply directly queries without delete existing nodes\n"
						+ "--inference=true/false -> apply inference rules (by default=true)\n"
						+ "Query files are in the folder \"cypherQueries\".");
				System.exit(0);
			}
			System.out.println("inputFile="+inputFile);

			GraphModeling gm = new GraphModeling ();
			if(!noDelete) {
				gm.graphSettings();
			}
			if(inference)
				gm.inference();
			gm.constraints();
			gm.statsQueries ("stats.cypher", "stats");
			gm.resultQueries ("results.cypher");
			gm.close();

		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
