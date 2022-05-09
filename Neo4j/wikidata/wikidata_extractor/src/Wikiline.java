import java.time.LocalDate;

public class Wikiline {
	String ID_from;
	String ID_to;
	String ID_o;
	String date_start;
	String date_end;
	boolean valid = false;
	float proba = 0.0f;
	
	String type;
	public Wikiline() {
		
	}

	public String extractString (String v) {
		v = v.substring(v.indexOf("\"") + 1);
		return v.substring(0, v.indexOf("\""));
	}

	public String extractDate (String d) throws Exception{
		String s = d.substring(2, 6)+"-"+d.substring(6,8)+"-01";
		LocalDate.parse(s);
		return s;
	}

	public float extractFloat (String f) {
		return new Float(f.substring(0, f.indexOf(")")).substring(1));
	}

	public String toString () {
		if(type.compareTo("sameAs") == 0)
			return type+";"+ID_from+"-"+ID_to+";"+ID_from+";"+ID_to;
		else
			return type+";"+
				ID_from+"-"+ID_to+"-"+ID_o+"-"+date_start+"-"+date_end+"-"+proba+";"+
				ID_from+";"+ID_to+";"+ID_o+";"+
				date_start+";"+date_end+";"+valid+";"+proba;
	}
}
