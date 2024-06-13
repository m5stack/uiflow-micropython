## sys file system directory structure

The system resource files of different boards will be automatically packed 
according to the board type when the file system is packed.

```bash
├── README.md  ----> this file
├── common     ----> common resource for all board
├── atoms3     ----> resource for atoms3 board
├── cores3     ----> resource for cores3 board
└── ...        ----> others board...
```