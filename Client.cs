namespace Курсач;

public class Client
{
    public string FirstName
    {
        get => firstName;
        set => firstName = value ?? throw new ArgumentNullException(nameof(value));
    }

    public string LastName
    {
        get => lastName;
        set => lastName = value ?? throw new ArgumentNullException(nameof(value));
    }

    public int Age
    {
        get => age;
        set => age = value;
    }

    public int PassNumber
    {
        get => passNumber;
        set => passNumber = value;
    }

    public List<Product> Products
    {
        get => products;
        set => products = value ?? throw new ArgumentNullException(nameof(value));
    }

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