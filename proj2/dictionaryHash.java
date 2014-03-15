package com.cornell.edu;
	
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.*;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import com.cornell.edu.WordSense;

public class dictionaryHash 
{

	private Map<WordSense, List<String>> dictionaryMap;
	
	public dictionaryHash(String dictionaryPath) throws ParserConfigurationException, SAXException, IOException 
	{
		dictionaryMap = new HashMap<WordSense, List<String>>();
		File dictionaryFile = new File(dictionaryPath);
		int entryNo=0;
		
		WordSense[] wordsenseArray;
		List<String> def= new ArrayList<String>();
		List<String> DictMinusStopWords= new ArrayList<String>();
		List<String> DictLemmatizedWords= new ArrayList<String>();
		
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = dbf.newDocumentBuilder();
		Document dictXml = builder.parse(dictionaryFile);

		NodeList allEntries = dictXml.getElementsByTagName("lexelt");
	
		for (int x = 0; x < allEntries.getLength(); x++) 
		{
			
			Element wordElement = (Element) allEntries.item(x);
			
			NodeList senseList = wordElement.getElementsByTagName("sense");
	
			for (int j = 0; j < senseList.getLength(); j++) {
				wordsenseArray[entryNo]=new WordSense();
				Element sense = (Element) senseList.item(j);
				String definition = sense.getAttribute("gloss");
			
				wordsenseArray[entryNo].word = wordElement.getAttribute("item");
				wordsenseArray[entryNo].sense = sense.getAttribute("id");;
			
				StringTokenizer st = new StringTokenizer(definition); 
				while (st.hasMoreTokens()) {
					def.add(st.nextToken());
				}
				DictMinusStopWords=RemoveStopWords(def);
				DictLemmatizedWords=Lemmatize(DictMinusStopWords);
			}
			
			dictionaryMap.put(wordsenseArray[entryNo], def );
		}
	}

}
	