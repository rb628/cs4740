import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;
import java.util.regex.*;

import edu.washington.cs.knowitall.morpha.MorphaStemmer;
import uk.ac.susx.informatics.Morpha;
import weka.core.Stopwords;

public class Dictionary {
	static List<String> Context = new ArrayList<String>();
	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader("C:\\Users\\rems\\Documents\\NLP\\p2\\training_data.data"));
		String sCurrentLine;
		
		//Retrieve the context words list surrounding the target word
		while ((sCurrentLine = br.readLine()) != null) {
		 List<String> ContextWords = new ArrayList<String>();
		 ContextWords = PatternMatch(sCurrentLine);   

		 //Exclude stop words in the context list
		 Context = RemoveStopWords(ContextWords);
		 //for(String word:Context){
		   //System.out.println(word);
         //}
		 //Lemmatize the words in the context list
		 Context = Lemmatize(Context);
	   	 System.out.println("Context is "+ Context);
	   	
	   	 
		}//End while
		
    }

	static List<String> PatternMatch(String sCurrentLine) {
		
		List<String> tokensVal = new ArrayList<String>();
		List<String> context = new ArrayList<String>();
		//Retrieve the example 
		Pattern p = Pattern.compile("^(\\w+\\.\\w)\\s+\\|\\s+(\\d)\\s+\\|\\s+(.*)");
		//Retrieve the context words surrounding the target word
		Pattern pContext = Pattern.compile("(.*)\\%%(.*)\\%%(.*)");
		Matcher m,mContext;
				
		m = p.matcher(sCurrentLine);
		if (m.find()) {
			tokensVal.add(m.group(3));
		}			
		
		for(String tokenContext:tokensVal){
  		  mContext = pContext.matcher(tokenContext); 
		  if(mContext.find()){
			  context.add(mContext.group(1)+ mContext.group(3));
		  }		
		}

		return context;
	 }
	
	static List<String> RemoveStopWords(List<String> ContextWords){
		String token;
		List<String> ContextWords1 = new ArrayList<String>();
		for(String word:ContextWords){
		 //System.out.println("word is "+ word);
		 StringTokenizer tokenizer = new StringTokenizer(word);
		 //System.out.println("tokenizer is "+ tokenizer.toString());
		 while (tokenizer.hasMoreTokens()) {
			 token = tokenizer.nextToken();
			 
			 if(!weka.core.Stopwords.isStopword(token)){
				 //	 System.out.println("stop word is "+ token);
				 String[] words = token.replaceAll("(\\p{P})|(\\``)|(\\d+)|(\\$)", " ").toLowerCase().split("\\s+");
		   	     for(String word1:words){
		   	    	 //		System.out.println("After removing punctuations"+ word1);
				    if(!word1.matches("^(\\w)||^(\\s)||^(\\w\\w)")){
				    	ContextWords1.add(word1);	
				    }
				 }	 //end for
			  } //end inner if
		   } //end while
		}//end main for
		
		return ContextWords1;
		
	 }
	
	static List<String> Lemmatize(List<String>ContextWords) {
		List<String> ContextWords1 = new ArrayList<String>();
		for(String word:ContextWords){
			new MorphaStemmer();
	 	    String morpha = MorphaStemmer.morpha(word,false);
			ContextWords1.add(morpha);
		}
		return ContextWords1;
		
	}
	
}
