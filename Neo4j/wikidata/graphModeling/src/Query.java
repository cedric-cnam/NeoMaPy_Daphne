/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */

public class Query {
	String instruction;
	String query;
	
	Query (String instruction, String query){
		this.instruction = instruction;
		this.query = query;
	}

	public String toString () {
		return "\n//"+instruction + "\n\t"+query;
	}
}
