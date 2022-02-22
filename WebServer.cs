using System.Net;
using System.Text;
using System.Text.Json;

namespace Курсач;

public class WebServer
{
    private static bool running = true;
    public static HttpListener listener;
    public Cashier cashier;
    public WebServer(Cashier cashier)
    {
        listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8081/");
        this.cashier = cashier;
    }
    
    public async Task GlobalHandler()
    {
        listener.Start();
        while (running)
        {
            HttpListenerContext ctx = await listener.GetContextAsync();
            HttpListenerRequest req = ctx.Request;
            HttpListenerResponse resp = ctx.Response;

            byte[] body = Encoding.UTF8.GetBytes("Error route");

            if (req.HttpMethod == "POST")
            {
                string postData = new StreamReader(req.InputStream).ReadToEnd();
                switch (req.Url.ToString())
                {
                    case "http://localhost:8081/clients/add":
                        try
                        {
                            Client newClient = JsonSerializer.Deserialize<Client>(postData);
                            cashier.clients.Add(newClient);
                            body = Encoding.UTF8.GetBytes("Data have written");
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine(e);
                            throw;
                        }
                        break;
                }
            } else if (req.HttpMethod == "GET")
            {
                switch (req.Url.ToString())
                {
                    case "http://localhost:8081/clients":
                        body = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(cashier.clients));
                        break;
                    case "http://localhost:8081/expired_products":
                        body = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(cashier.expiredProducts));
                        break;
                }
            }
            
            resp.ContentType = "text/json";
            resp.ContentEncoding = Encoding.UTF8;
            resp.ContentLength64 = body.LongLength;
            
            await resp.OutputStream.WriteAsync(body, 0, body.Length);
            resp.Close();
        }
    }
}