package neoMaPy.connection;

import java.util.List;

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

import neoMaPy.NeoMaPy;
import neoMaPy.Query;
import neoMaPy.ui.NeoMaPyGraph;

public class Connection implements AutoCloseable {
	private final Driver driver;

	public Connection() throws Exception {
		Config config = Config.builder().build();
		driver = GraphDatabase.driver((String) NeoMaPy.config.get("URI"),
				AuthTokens.basic((String) NeoMaPy.config.get("user"), (String) NeoMaPy.config.get("mdp")), config);
	}

	@Override
	public void close() throws Exception {
		driver.close();
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
						System.out.println(q.instruction);
					}
					return 1;
				}
			});
		}
		System.out.println("Graph Loaded");
	}

	@SuppressWarnings("unchecked")
	private JSONObject toJSON(Record r) {
		JSONObject o = new JSONObject();
		for (String k : r.keys()) {
			o.put(k, r.get(k));
		}

		return o;
	}

}
