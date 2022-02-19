namespace Курсач;



public class Client
{
    private int id;
    public string firstName, lastName;
    public int age, passNumber;
    public List<Product> products;

    public Client(string firstName, string lastName, int age, int passNumber)
    {
        this.firstName = firstName;
        this.lastName = lastName;
        this.age = age;
        this.passNumber = passNumber;
        products = new List<Product>();
    }
}