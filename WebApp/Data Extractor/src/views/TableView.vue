<script>
export default {
  props: ['id'],
  data() {
    return {
      file: '',
      content: [],
      parsed: false,
    }
  },
  methods: {
  },
  mounted() {
    console.log(this.$store.state.csvString)
    var lines = this.$store.state.csvString.split("\n"),
      output = [],
      i;
    for (i = 0; i < lines.length; i++)
      output.push("<tr><td>"
        + lines[i].slice(0, -1).split(",").join("</td><td>")
        + "</td></tr>");
    output = "<table class='table'>" + output.join("") + "</table>";
    var table = document.getElementById("table-wrapper")
    table.innerHTML = output
  }
}

</script>

<template>
  <div id="table-wrapper">

  </div>
</template>

<style>
* {
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
}

body {
  font-family: Helvetica;
  -webkit-font-smoothing: antialiased;
}

h2 {
  text-align: center;
  font-size: 18px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: white;
  padding: 30px 0;
}

/* Table Styles */

#table-wrapper {
  position: absolute;
  transform: translateX(-50%);
  left: 50%;
  top: 20%;
  box-shadow: 0 1.25em 3.43em rgba(0, 0, 0, 0.08);
}

.table {
  border-radius: 5px;
  font-size: 12px;
  font-weight: normal;
  border: none;
  border-collapse: collapse;
  width: 100%;
  max-width: 100%;
  white-space: nowrap;
  background-color: #181818;
}

.table td,
.table th {
  text-align: center;
  padding: 8px;
}

.table td {
  border: #E6E4E4 1px solid;
  font-size: 12px;
}

.table thead th {
  color: blue;
  background: pink;
}


.table thead th:nth-child(odd) {
  color: green;
  background: pink;
}

.table tr:nth-child(even) {
  color: #fccb06;
  background: #181818;
}

/* Responsive */

@media (max-width: 767px) {
  .fl-table {
    display: block;
    width: 100%;
  }

  .table-wrapper:before {
    content: "Scroll horizontally >";
    display: block;
    text-align: right;
    font-size: 11px;
    color: white;
    padding: 0 0 10px;
  }

  .fl-table thead,
  .fl-table tbody,
  .fl-table thead th {
    display: block;
  }

  .fl-table thead th:last-child {
    border-bottom: none;
  }

  .fl-table thead {
    float: left;
  }

  .fl-table tbody {
    width: auto;
    position: relative;
    overflow-x: auto;
  }

  .fl-table td,
  .fl-table th {
    padding: 20px .625em .625em .625em;
    height: 60px;
    vertical-align: middle;
    box-sizing: border-box;
    overflow-x: hidden;
    overflow-y: auto;
    width: 120px;
    font-size: 13px;
    text-overflow: ellipsis;
  }

  .fl-table thead th {
    text-align: left;
    border-bottom: 1px solid #f7f7f9;
  }

  .fl-table tbody tr {
    display: table-cell;
  }

  .fl-table tbody tr:nth-child(odd) {
    background: none;
  }

  .fl-table tr:nth-child(even) {
    background: transparent;
  }

  .fl-table tr td:nth-child(odd) {
    background: #F8F8F8;
    border-right: 1px solid #E6E4E4;
  }

  .fl-table tr td:nth-child(even) {
    border-right: 1px solid #E6E4E4;
  }

  .fl-table tbody td {
    display: block;
    text-align: center;
  }
}</style>