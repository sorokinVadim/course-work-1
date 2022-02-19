// See https://aka.ms/new-console-template for more information

// Ломбард. База збережених товарів і нерухомості: анкетні дані клієнта,
//     найменування товару, оціночна вартість; сума, видана під заставу, дата здачі,
// термін зберігання. Операції прийому товару, повернення, продажу після
//     закінчення терміну зберігання

using System.Data.Common;
using Курсач;
using MySql.Data.MySqlClient;

class Program
{
    public static void Main()
    {
        Cashier cashier = new Cashier();
        Client client = new Client("Vadim", "Sorokin", 18, 2133123);
        client.products.Add(new Product("Laptop", 1000, 900, 30));
        cashier.clients.Add(client);
        Console.WriteLine(client.firstName);
        string sqlLogin = "Database=test;Data Source=localhost;User Id=sorokin;Password=1234";
        MySqlConnection connection = new MySqlConnection(sqlLogin);
        connection.Open();
        MySqlCommand cmd = new MySqlCommand("SELECT * FROM test.ingredients;", connection);
        using (DbDataReader reader = cmd.ExecuteReader())
        {
            if (reader.HasRows)
            {
                while (reader.Read())
                {   
                    Console.Write(reader.GetOrdinal("id"));
                    int nameIndex = reader.GetOrdinal("name");
                    string empName = reader.GetString(nameIndex);
                    Console.WriteLine(empName);
                }
            }
        }
    }
}
