/**
 * Created by Nicolas Travers <nicolas.travers@devinci.fr> 2022-2023©
 */
import java.time.LocalDate;

public class Wikiline {
	String ID_s;
	String ID_o;
	String ID_p;
	String date_start;
	String date_end;
	boolean valid = false;
	float proba = 0.0f;

	boolean polarity = true;
	
	String type;
	public Wikiline() {
		
	}

	public String extractString (String v) {
		v = v.substring(v.indexOf("\"") + 1);
		return v.substring(0, v.indexOf("\""));
	}

	public String extractDate (String d) throws Exception{
		String s = "";
		if(d.startsWith(" \"-")) {
			String year = d.substring(3, 7);
			String month = "01";
			s = year+"-"+month+"-01";
			LocalDate.parse(s);
			
		} else {
			String year = d.substring(2, 6);
			String month = d.substring(6,8);
			if(month.compareTo("00") == 0)
				month = "01";
			if(year.compareTo("0000") == 0)
				s = "0000-01-01";
			else
				s = year+"-"+month+"-01";
			LocalDate.parse(s);			
		}
		return s;
	}

	public float extractFloat (String f) {
		return new Float(f.substring(0, f.indexOf(")")).substring(1));
	}

	public String toString () {
		if(type.compareTo("sameAs") == 0)
			return type+";"+ID_s+"-"+ID_p+";"+ID_s+";"+ID_p;
		else
			return type+";"+
				ID_s+"-"+ID_o+"-"+ID_p+"-"+date_start+"-"+date_end+"-"+proba+";"+
				ID_s+";"+ID_o+";"+ID_p+";"+
				date_start+";"+date_end+";"+valid+";"+proba+";"+polarity;
	}
}
