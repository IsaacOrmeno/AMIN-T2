import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import javafx.util.Pair;

import java.io.File;

public class Colonia_Hormiga 
{
	public static void main(String[] args) throws FileNotFoundException, IOException
	{
		 String Nombre_Archivo=args[0];
		 File fichero = new File(Nombre_Archivo); 
		 
		 try 
		 {
			 String Ruta_Archivo = fichero.getAbsolutePath();
			 FileReader f = new FileReader(Ruta_Archivo);
			 BufferedReader b = new BufferedReader(f);
			 String Name = b.readLine().split(":")[1].trim();
			 String Type = b.readLine().split(":")[1].trim();
			 String Comment =  b.readLine().split(":")[1].trim();
			 int Dimension = Integer.parseInt( b.readLine().split(":")[1].trim() );
			 String Edge_Weight_Type = b.readLine().split(":")[1].trim();
			 b.readLine();
			 		 
			 String Cadena;
			 String x, y;
			 float X, Y;
			 
			 ArrayList< Pair<Float,Float> > Lista_Coordenadas = new ArrayList< Pair<Float,Float> >() ;
			 
			 while((Cadena = b.readLine()).contains("EOF")==false)
			 {
				 x =Cadena.split(" ")[1].trim();
				 X =Float.parseFloat(x);
				 
				 y =Cadena.split(" ")[2].trim();
				 Y =Float.parseFloat(y);
				 
				 Lista_Coordenadas.add(new Pair(X,Y));
			 }
			 b.close();
		 
		 
		 }
		 catch(FileNotFoundException e)
		 {
	         System.out.println("El Archivo no se ha Encontrado, verifique ekl nombre  y no olvide la extension .txt luego de este. Ejemplo: berlin52.txt ");
	     }
		 
		 
		 
		 String semilla = args[1];
		 int Semilla = Integer.parseInt(semilla);
		 
		 String tamano_colonia = args[1];
		 int Tamano_Colonia = Integer.parseInt(tamano_colonia);
		 
		 String iteraciones = args[2];
		 int Iteraciones = Integer.parseInt(iteraciones);
		 
		 String alpha = args[3];
		 float Alpha = Float.parseFloat(alpha);
		 
		 String qcero = args[4];
		 float qCero = Float.parseFloat(qcero);
		 
		 String beta = args[5];
		 float Beta = Float.parseFloat(beta);
		 
	}
}
