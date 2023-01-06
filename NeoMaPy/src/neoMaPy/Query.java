package neoMaPy;

public class Query {
	public String instruction;
	public String query;

	Query(String instruction, String query) {
		this.instruction = instruction;
		this.query = query;
	}

	public String toString() {
		return "\n//" + instruction + "\n\t" + query;
	}
}
