package neoMaPy.connection;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
import org.neo4j.driver.exceptions.ClientException;
import org.neo4j.driver.internal.value.IntegerValue;

import neoMaPy.NeoMaPy;
import neoMaPy.Query;
import neoMaPy.ui.graphstream.NeoMaPyGraph;

public class Connection implements AutoCloseable {
	private static Driver driver;

	public Connection() {
	}

	public boolean connect () {
		Config config = Config.builder().build();
		try{
			driver = GraphDatabase.driver((String) NeoMaPy.config.get("URI"),
					AuthTokens.basic((String) NeoMaPy.config.get("user"), (String) NeoMaPy.config.get("mdp")), config);
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}
	
	@Override
	public void close() throws Exception {
		driver.close();
	}

	public static Map<String, Integer> loadStats(List<Query> queries) {
		Map<String, Integer> values = new HashMap<String, Integer> ();
		try (Session session = driver.session()) {
			session.readTransaction(new TransactionWork<Integer>() {
				@Override
				public Integer execute(Transaction tx) {
					for (Query q : queries) {
						Result result = tx.run(q.query);
						while (result.hasNext()) {
							Record r = result.next();
							JSONObject json = toJSON(r);
							values.put(q.instruction, ((IntegerValue)json.get("NB")).asInt());
						}
					}
					return 1;
				}
			});
		}
		return values;
	}

	public static boolean updateQuery (String query) throws ClientException {
		try (Session session = driver.session()) {
			session.writeTransaction(new TransactionWork<Integer>() {
				@Override
				public Integer execute(Transaction tx) {
					tx.run(query);
					return 1;
				}
			});
			return true;
		}
	}
	
	public void loadGraph(List<Query> queries, NeoMaPyGraph graph) {
		try (Session session = driver.session()) {
			session.readTransaction(new TransactionWork<Integer>() {
				@Override
				public Integer execute(Transaction tx) {
					for (Query q : queries) {
						Result result = tx.run(q.query);
						while (result.hasNext()) {
							Record r = result.next();
							JSONObject json = toJSON(r);
							graph.add2Graph(q, json);
						}
					}
					return 1;
				}
			});
		}
	}

	@SuppressWarnings("unchecked")
	private static JSONObject toJSON(Record r) {
		JSONObject o = new JSONObject();
		for (String k : r.keys()) {
			o.put(k, r.get(k));
		}

		return o;
	}

}