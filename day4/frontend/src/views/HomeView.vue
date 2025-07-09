<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png">
      <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <div v-if="this.category === ''" class="No-category-container">
      <p>No Category found</p>
      <br />
      <h1
        style="cursor: pointer"
        v-on:click="this.$router.push({ name: 'addCategory' })"
      >
        Add the first category
      </h1>
    </div>
    <div v-else class="category-container">
      <h1>Category List</h1>
      <button
        v-on:click="this.$router.push({ name: 'addCategory' })"
        class="add-category-button"
      >
        Add a new Category
      </button>
      <br><br>
    <table>
      <thead>
        <th>ID</th>
        <th>Name</th>
        <th>Description</th>
        <th>Status</th>
        <th>Created_by</th>
        <th>updated_by</th>
        <th>Created_at</th>
        <th>updated_at</th>
        <th>Delete-status</th>
        <th>Action</th>
      </thead>
      <tbody>
        <tr v-for="i in category">
          <td>{{ i.id }}</td>
          <td>{{ i.name }}</td>
          <td>{{ i.description }}</td>
          <td>{{ i.status }}</td>
          <td>{{ i.created_by }}</td>
          <td>{{ i.updated_by }}</td>
          <td>{{ i.created_at }}</td>
          <td>{{ i.updated_at }}</td>
          <td>{{ i.delete }}</td>
          <td>
            <a style="cursor: pointer;"
              v-on:click="this.$router.push({ name: 'editCategory', params: { id: i.id } })"
            >
              Edit
          </a> | 
            <a style="cursor: pointer;"
              v-on:click="this.deleteCategory(i.id)"
            >
              Delete
        </a>
          </td>
        </tr>
      </tbody>
    </table>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import axios from "axios";
export default {
  name: "HomeView",
  components: {
    HelloWorld,
  },
  data() {
    return {
      category: "",
      token: "",
    };
  },
  created() {
    this.token = localStorage.getItem("authToken");
    if (!this.token) {
      this.$router.push("/login");
    } else {
      this.getCategory();
    }
  },
  methods: {
    getCategory() {
      axios
        .get("http://localhost:5000/category", {
          headers: {
            Authorization: `${this.token}`,
          },
        })
        .then((response) => {
          if (response.status === 200 && response.data.category_data) {
            this.category = response.data.category_data;
          }
        })
        .catch((error) => {
          this.category = "No category found";
          alert("Error fetching categories: " + error.message);
        });
    },
    deleteCategory(id) {
      if (confirm("Are you sure you want to delete this category?")) {
        axios
          .delete(`http://localhost:5000/category/${id}`, {
            headers: {
              Authorization: `${this.token}`,
            },
          })
          .then((response) => {
            if (response.status === 201) {
              alert("Category deleted successfully!");
              this.getCategory();
            } else {
              alert("Failed to delete category: " + response.data.message);
            }
          })
          .catch((error) => {
            alert("Error deleting category: " + error.message);
          });
      }
    },
  },
};
</script>
