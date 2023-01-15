package neoMaPy.ui.graphstream;

import java.time.ZonedDateTime;
import java.util.HashMap;
import java.util.Map;

import org.graphstream.graph.Edge;
import org.graphstream.graph.Node;
import org.graphstream.graph.implementations.MultiGraph;
import org.json.simple.JSONObject;
import org.neo4j.driver.internal.value.BooleanValue;
import org.neo4j.driver.internal.value.DateTimeValue;
import org.neo4j.driver.internal.value.FloatValue;
import org.neo4j.driver.internal.value.NullValue;
import org.neo4j.driver.internal.value.StringValue;

import neoMaPy.Query;

public class NeoMaPyGraph extends MultiGraph {
	// public Map<String, Integer> edgeAttributes = new HashMap<String, Integer> ();

	public NeoMaPyGraph(String graphID) {
		super(graphID);
	}

	public void css() {
		this.setAttribute("ui.stylesheet", "url('file://conf/NeoMaPy.css')");
	}

	public void add2Graph(Query q, JSONObject json) {
		if (q.instruction.endsWith("nodes"))
			addNodes(json);
		else if (q.instruction.startsWith("TF links"))
			addTF(json);
		else if (q.instruction.startsWith("TF conflict"))
			addConflict(json);
		else if (q.instruction.startsWith("TF inference"))
			addInference(json);
		else
			return;
	}

	private void addAttribute(Object o, String attribute, String value) {
		if (attribute == null)
			return;
		if (o instanceof Node)
			((Node) o).setAttribute(attribute, value);
		else if (o instanceof Edge)
			((Edge) o).setAttribute(attribute, value);
		/*
		 * Integer nb = edgeAttributes.get(value); if(nb == null) { nb = 1; } else nb++;
		 * edgeAttributes.put(value, nb);
		 */
	}

	public void addNodes(JSONObject json) {
		String nodeId = (String) getNeo4jValue(json, "Node_id");
		Node n = addNodeById(nodeId);
		if (json.get("Node_name") != null) {
			n.setAttribute("name", getStringNeo4j(json, "Node_name"));
			// "concept "+
			n.setAttribute("ui.long-text", getStringNeo4j(json, "Node_name"));

		}
		addAttribute(n, "ui.class", getStringNeo4j(json, "Node_type"));
		n.setAttribute("type", getStringNeo4j(json, "Node_type"));
		// System.out.println("ui.class: "+json.get("Node_name").toString() + " /
		// "+json.get("Node_type").toString());
	}

	public void addTF(JSONObject json) {
		String nodeId = (String) getNeo4jValue(json, "Node_id");
		Node n = addNodeById(nodeId);
		n.setAttribute("date_start", (ZonedDateTime) getNeo4jValue(json, "date_start"));
		n.setAttribute("date_end", (ZonedDateTime) getNeo4jValue(json, "date_end"));
		n.setAttribute("polarity", getBooleanNeo4j(json, "polarity"));
		n.setAttribute("valid", getBooleanNeo4j(json, "valid"));
		double weight = getDoubleNeo4j(json, "weight");
		n.setAttribute("weight", weight);
		setSize(nodeId, weight);

		String type = getStringNeo4j(json, "type");
		n.setAttribute("type", "TF"+(type != null ? "_"+type:""));
		addAttribute(n, "ui.class", "TF");
		Object o = getNeo4jValue(json, "valid");
		if(o != null && !((Boolean)o))
			addAttribute(n, "ui.class", "TF_invalid");
		else if (weight > 1000000)
			addAttribute(n, "ui.class", "TF_infinite");
		else
			addAttribute(n, "ui.class", "TF");

		addEdge(json, nodeId, "s");
		addEdge(json, nodeId, "o");
		addEdge(json, nodeId, "p");
	}

	public void addConflict(JSONObject json) {
		String from = getStringNeo4j(json, "from");
		String to = getStringNeo4j(json, "to");
		String type = getStringNeo4j(json, "type");
		String edgeId = edgeId(from, to);
		try {
			Edge e = addEdge(edgeId, type, from, to);
			addConsistency(e, json, "pCon");
			addConsistency(e, json, "pInc");
			addConsistency(e, json, "tInc");
		} catch (org.graphstream.graph.EdgeRejectedException e) {
			System.out.println(edgeId);
		}
	}

	public void addInference(JSONObject json) {
		String from = getStringNeo4j(json, "from");
		String to = getStringNeo4j(json, "to");
		String edgeId = edgeId(from, to);
		try {
			Edge e = addEdge(edgeId, "inference", from, to);
		} catch (org.graphstream.graph.EdgeRejectedException e) {
			System.out.println(edgeId);
		}
	}

	private void setSize(String nodeId, double size) {
		Node n = addNodeById(nodeId);
		if (size < 10)
			n.setAttribute("ui.size", size * 5);
		else
			n.setAttribute("ui.size", 50);
	}

	private Node addNodeById(String nodeId) {
		Node n = this.getNode(nodeId);
		if (n == null)
			n = this.addNode(nodeId);
		return n;
	}

	private String edgeId(String from, String to) {
		if (from.compareTo(to) < 0)
			return from + "_" + to;
		else
			return to + "_" + from;
	}

	private Edge addEdge(JSONObject json, String from, String type) {
		String to = getStringNeo4j(json, type);
		String edgeId = edgeId(from, to);
		try {
			Edge e = addEdge(edgeId, type, from, to);
			return e;
		} catch (org.graphstream.graph.EdgeRejectedException e) {
			System.out.println(edgeId);
			return null;
		}
	}

	private Edge addEdge(String id, String type, String from, String to)
			throws org.graphstream.graph.EdgeRejectedException {
		addNodeById(from);
		addNodeById(to);
		if (this.getEdge(id) == null)
			this.addEdge(id, from, to);
		Edge e = this.getEdge(id);
		e.setAttribute(type, true);
		addAttribute(e, "ui.class", type);
		return e;
	}

	private void addConsistency(Edge e, JSONObject json, String type) {
		Object o = getNeo4jValue(json, type);
		if (o != null) {
			e.setAttribute(type, (Boolean) o);
			addAttribute(e, "ui.class", "TC1_"+type);
		}
	}

	public String getStringNeo4j(JSONObject json, String att) {
		Object o = getNeo4jValue(json, att);
		if(o == null)
			return null;
		return (String)o ;
	}

	public Boolean getBooleanNeo4j(JSONObject json, String att) {
		Object o = getNeo4jValue(json, att);
		if(o == null)
			return null;
		return (Boolean)o;
	}

	public Double getDoubleNeo4j(JSONObject json, String att) {
		Object o = getNeo4jValue(json, att);
		if(o == null)
			return null;
		return (Double)o;
	}

	public Object getNeo4jValue(JSONObject json, String att) {
		Object o = json.get(att);
		if (o instanceof StringValue)
			return ((StringValue) o).asString();
		else if (o instanceof BooleanValue)
			return ((BooleanValue) o).asBoolean();
		else if (o instanceof FloatValue)
			return ((FloatValue) o).asDouble();
		else if (o instanceof DateTimeValue)
			return ((DateTimeValue) o).asZonedDateTime();
		else if (o instanceof NullValue)
			return null;
		return o;
	}

	public void countAttributes() {

		Map<String, Integer> nodeAttributes = new HashMap<String, Integer>();
		nodes().forEach(n -> {
			n.attributeKeys().forEach(att -> {
				Integer val = nodeAttributes.get(att);
				if (val == null)
					val = 1;
				else
					val++;
				nodeAttributes.put(att, val);
			});

		});
		System.out.println("Nodes: " + nodeAttributes);

		Map<String, Integer> edgeAttributes = new HashMap<String, Integer>();
		edges().forEach(n -> {
			n.attributeKeys().forEach(att -> {
				Integer val = edgeAttributes.get(att);
				if (val == null)
					val = 1;
				else
					val++;
				edgeAttributes.put(att, val);
			});

		});
		System.out.println("Edges: " + edgeAttributes);
	}
}
