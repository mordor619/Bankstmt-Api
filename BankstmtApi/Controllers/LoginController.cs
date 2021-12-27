using BankstmtApi.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BankstmtApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class LoginController : ControllerBase
    {
        private readonly IConfiguration _configuration;

        private IMongoCollection<UserLogin> users;

        public LoginController(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        [HttpGet]
        [Route("getAllUsers")]
        public JsonResult getAllUsers()
        {
            MongoClient mongoClient = new MongoClient(_configuration.GetConnectionString("con1"));

            var dbList = mongoClient.GetDatabase("bankstatement")
                .GetCollection<UserLogin>("userlogin")
                .AsQueryable();

            return new JsonResult(dbList);
        }

        [HttpGet]
        [Route("LoginBankUser")]
        public IActionResult LoginBankUser(string username, string password)
        {
            MongoClient mongoClient = new MongoClient(_configuration.GetConnectionString("con1"));

            users = mongoClient.GetDatabase("bankstatement")
                .GetCollection<UserLogin>("userlogin");

            List<UserLogin> userList = users.Find(user => true).ToList();

            foreach(var u in userList)
            {
                if(u.username.Equals(username) && u.password.Equals(password))
                {
                    return Ok(u.username);
                }
            }

            string resStr = "nota";
            return Ok(resStr);
        }

    }
}
