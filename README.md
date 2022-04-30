## Motivation

This is an alternative to airflow. Unfortunately, the following setbacks occur while setting up airflow:

| Airflow's Provisions                                             | Current Developments            |
|------------------------------------------------------------------|---------------------------------|
| GUI intensive                                                    | GUI not needed.                 |
| Supports Linux / macOS natively. Windows Support for Docker ONLY | Using Windows OS                |
| Latest version of airflow requires library SQLAlchemy <1.4       | Using 1.4.2                     |
| Python 3.10 only be supported in Airflow 2.3                     | Using 3.10                      |
| Must `docker-compose build` to reinstall pip                     | Updates internal packages often |

Our solution is to bootstrap our own worker container which will execute our tasks.
In the future, once current developments align with Airflow's provisions, we will reconsider choices.

