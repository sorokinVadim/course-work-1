namespace Курсач;


public class Cashier
{
    public List<Client> clients;

    public List<Client> Clients
    {
        get => clients;
        set => clients = value ?? throw new ArgumentNullException(nameof(value));
    }

    public List<Product> ExpiredProducts
    {
        get => expiredProducts;
        set => expiredProducts = value ?? throw new ArgumentNullException(nameof(value));
    }

    public List<Product> expiredProducts;

    public Cashier()
    {
        clients = new List<Client>();
        expiredProducts = new List<Product>();
    }

    public void CheckExpired()
    {
        bool isExpired;
        foreach (Client client in clients)
        {
            foreach (Product procuct in client.products)
            {
                isExpired = procuct.savingsTerm < DateTime.Now;
                if (isExpired)
                {   expiredProducts.Add(procuct);
                    client.products.Remove(procuct);
                }
            }
        }
    } 

}