using MongoDB.Bson;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BankstmtApi.Models
{
    public class UserLogin
    {
        public ObjectId Id { get; set; }

        public string username { get; set; }

        public string password{ get; set; }
    }
}
