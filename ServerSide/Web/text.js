const pg = require('pg');

const config =  {
            user: "postgres",
            host: "localhost",
            database: "B03",
            password: "123456",
            port: 5432
        }

const client = new pg.Client(config);

client.connect(err => {
    if (err) throw err;
    else {
        queryDatabase();
    }
});

function queryDatabase() {
    const query = 'SELECT * FROM "B03_Coffee"."Samples"';

    client
        .query(query)
        .then(() => {
            console.log('Table created successfully!');
            client.end(console.log('Closed client connection'));
        })
        .catch(err => console.log(err))
        .then(() => {
            console.log('Finished execution, exiting now');
            process.exit();
        });
}
