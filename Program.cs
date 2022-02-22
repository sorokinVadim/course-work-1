using System.Net;
using System.Net.Mime;
using System.Text;
using System.Text.Json;
using Курсач;

class Program
{
    public static HttpListener listener;
    public static string url = "http://localhost:8081/";
    public static Cashier cashier;

    public static async Task HandleIncomingConnections()
    {
        while (true)
        {
            HttpListenerContext ctx = await listener.GetContextAsync();
            HttpListenerRequest req = ctx.Request;
            HttpListenerResponse resp = ctx.Response;
            string bodyData = "Nothing";
            Console.WriteLine(req.Url);
            switch (req.Url.ToString())
            {
                case "http://localhost:8081/expired_products":
                    bodyData = JsonSerializer.Serialize(cashier.expiredProducts);
                    break;
                case "http://localhost:8081/clients":
                    bodyData = JsonSerializer.Serialize(cashier.clients);
                    break;
                case "http://localhost:8081/clients/add":
                    var inDataClient = new StreamReader(req.InputStream, req.ContentEncoding);
                    var deserializeClient = JsonSerializer.Deserialize<Client>(inDataClient.ReadToEnd());
                    // Console.WriteLine(deserializeClient);
                    cashier.clients.Add(deserializeClient);
                    break;
            }
            
            byte[] body = Encoding.UTF8.GetBytes(bodyData);

            resp.ContentType = "text/json";
            resp.ContentEncoding = Encoding.UTF8;
            resp.ContentLength64 = body.LongLength;
            
            await resp.OutputStream.WriteAsync(body, 0, body.Length);
            resp.Close();
        }
    }


    public static void Main()
    {
        cashier = new Cashier();
        cashier.clients.Add(new Client("Vadim", "Sorokin", 30, 12341234));
        
        // Create a Http server and start listening for incoming connections
        listener = new HttpListener();
        listener.Prefixes.Add(url);
        listener.Start();
        Console.WriteLine("Listening for connections on {0}", url);
        
        // Handle requests
        Task listenTask = HandleIncomingConnections();
        listenTask.GetAwaiter().GetResult();
        
        // Close the listener
        listener.Close();
        
    }
}