using System.Net;
using System.Net.Mime;
using System.Text;
using System.Text.Json;
using Курсач;

class Program
{
    public static void Main()
    {
        Cashier cashier = new Cashier();
        string savedData;
        try
        {
            savedData = new StreamReader("Data.json").ReadToEnd();
            cashier = JsonSerializer.Deserialize<Cashier>(savedData);
        }
        catch (Exception e)
        {
            // cashier = new Cashier();
            Console.WriteLine(e);
            // throw;
        }

        var server = new WebServer(cashier);
        Task listenTast = server.GlobalHandler();
        listenTast.GetAwaiter().GetResult();
        
        WebServer.listener.Close();
        
        // // Create a Http server and start listening for incoming connections
        //
        // listener.Start();
        // Console.WriteLine("Listening for connections on {0}", url);
        //
        // // Handle requests
        // Task listenTask = HandleIncomingConnections();
        // listenTask.GetAwaiter().GetResult();
        //
        // // Close the listener
        // listener.Close();

        savedData = JsonSerializer.Serialize(server.cashier);
        var saverData = new StreamWriter("Data.json");
        saverData.Write(savedData);
        saverData.Flush();
        saverData.Close();
    }
}