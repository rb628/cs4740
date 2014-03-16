package com.cornell.edu;

import java.io.IOException;

import javax.xml.parsers.ParserConfigurationException;

import org.xml.sax.SAXException;

public class dict
{
	
	public static void main(String[] args) throws ParserConfigurationException, SAXException, IOException
	{
		try
		{
		dictionaryHash hash= new dictionaryHash("C:\\Users\\rems\\Documents\\NLP\\p2\\dictionary_sample.xml");
		hash.ReadData("C:\\Users\\rems\\Documents\\NLP\\p2\\training_sample.data");
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}
}
