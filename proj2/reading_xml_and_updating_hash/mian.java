package com.cornell.edu;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.xml.sax.SAXException;

import com.cornell.edu.dictionaryHash;

public class mian
{
	public static void main(String[] args) throws ParserConfigurationException, SAXException, IOException
	{
		//Path p1 = Paths.get("E:/NLP/Project2/dictionary.xml");
		try
		{
		dictionaryHash hash= new dictionaryHash("E:/NLP/dictionary.xml");
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
	}
}
