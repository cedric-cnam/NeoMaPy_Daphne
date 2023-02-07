/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
package neoMaPy;

public class Query {
	public String instruction;
	public String query;

	Query(String instruction, String query) {
		this.instruction = instruction;
		this.query = query;
	}

	@Override
	public String toString() {
		return "\n//" + instruction + "\n\t" + query;
	}
}
