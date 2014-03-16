package com.cornell;
	
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import com.cornell.WordSense;

import edu.washington.cs.knowitall.morpha.MorphaStemmer;

public class dictionaryHash 
{

	public Map<WordSense, List<String>> dictionaryMap;
	static List<String> Context = new ArrayList<String>();
	public dictionaryHash(String dictionaryPath) throws ParserConfigurationException, SAXException, IOException 
	{
		dictionaryMap = new HashMap<WordSense, List<String>>();
		File dictionaryFile = new File(dictionaryPath);
		int entryNo=0;
		
		WordSense[] wordsenseArray = new WordSense[9];
		List<String> def= new ArrayList<String>();
		List<String> DictMinusStopWords= new ArrayList<String>();
		List<String> DictLemmatizedWords= new ArrayList<String>();
		
		
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = dbf.newDocumentBuilder();
		Document dictXml = builder.parse(dictionaryFile);
		
		NodeList allEntries = dictXml.getElementsByTagName("lexelt");
		
		for (int x = 0; x < allEntries.getLength(); x++) 
		{
			wordsenseArray[entryNo]= new WordSense();
			Element wordElement = (Element) allEntries.item(x);
            
			wordsenseArray[entryNo].word = (String)wordElement.getAttribute("item");
			
			NodeList senseList = wordElement.getElementsByTagName("sense");
			
			for (int j = 0; j < senseList.getLength(); j++) {
				def.clear();
				
				wordsenseArray[entryNo]=new WordSense();
				
				Element sense1 = (Element) senseList.item(j);
			
				String definition = (String)sense1.getAttribute("gloss");
				
				wordsenseArray[entryNo].sense = sense1.getAttribute("id");
				
				StringTokenizer st = new StringTokenizer(definition); 
				while (st.hasMoreTokens()) {
					def.add(st.nextToken());
				}
				System.out.println("Def is "+def);
				DictMinusStopWords=RemoveStopWords(def);
				DictLemmatizedWords=Lemmatize(DictMinusStopWords);
				
				System.out.println("After Lemma is "+DictLemmatizedWords);
				System.out.println("Sense is "+wordsenseArray[entryNo].word);
				dictionaryMap.put(wordsenseArray[entryNo], DictLemmatizedWords);
				entryNo++;	
			    
			}
			 
		}
		for (Map.Entry entry : dictionaryMap.entrySet()) {
		    System.out.print("key,val: ");
		    //System.out.println((entry.getKey()).GetWord() + "," + entry.GetSense());
		}

		
	}
	
	public void ReadData(String filename) throws IOException{
		BufferedReader br = new BufferedReader(new FileReader(filename));
		String sCurrentLine;
	    //Retrieve the context words list surrounding the target word
		
		while ((sCurrentLine = br.readLine()) != null) {
				 List<String> ContextWords = new ArrayList<String>();
				 ContextWords = PatternMatch(sCurrentLine);   

				 //Exclude stop words in the context list
				 Context = RemoveStopWords(ContextWords);
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
	