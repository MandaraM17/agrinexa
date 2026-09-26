const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
require("dotenv").config();

const User = require("./models/User");

const app = express();

app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;

// Authentication middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({
      message: "Please login first"
    });
  }

  const token = authHeader.split(" ")[1];

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({
        message: "Invalid or expired token"
      });
    }

    req.user = user;
    next();
  });
}

// Home route
app.get("/", (req, res) => {
  res.json({
    message: "AgriNexa Backend is running"
  });
});

// REGISTER
app.post("/api/register", async (req, res) => {
  try {
    const {
      name,
      location,
      phone,
      email,
      password,
      role
    } = req.body;

    if (
      !name ||
      !location ||
      !phone ||
      !email ||
      !password ||
      !role
    ) {
      return res.status(400).json({
        message: "Please fill all required fields"
      });
    }

    if (!["farmer", "buyer", "worker"].includes(role)) {
      return res.status(400).json({
        message: "Invalid user role"
      });
    }

    if (password.length < 6) {
      return res.status(400).json({
        message: "Password must be at least 6 characters"
      });
    }

    const existingUser = await User.findOne({
      email: email.toLowerCase()
    });

    if (existingUser) {
      return res.status(409).json({
        message: "Email already registered"
      });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await User.create({
      name,
      location,
      phone,
      email,
      password: hashedPassword,
      role
    });

    const token = jwt.sign(
      {
        id: user._id,
        role: user.role
      },
      process.env.JWT_SECRET,
      {
        expiresIn: "7d"
      }
    );

    res.status(201).json({
      message: "Registration successful",
      token,
      user: {
        id: user._id,
        name: user.name,
        location: user.location,
        phone: user.phone,
        email: user.email,
        role: user.role
      }
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      message: "Registration failed"
    });
  }
});

// LOGIN
app.post("/api/login", async (req, res) => {
  try {
    const { email, password, role } = req.body;

    if (!email || !password || !role) {
      return res.status(400).json({
        message: "Email, password and role are required"
      });
    }

    const user = await User.findOne({
      email: email.toLowerCase(),
      role
    });

    if (!user) {
      return res.status(401).json({
        message: "Invalid email, password or role"
      });
    }

    const passwordMatch = await bcrypt.compare(
      password,
      user.password
    );

    if (!passwordMatch) {
      return res.status(401).json({
        message: "Invalid email, password or role"
      });
    }

    const token = jwt.sign(
      {
        id: user._id,
        role: user.role
      },
      process.env.JWT_SECRET,
      {
        expiresIn: "7d"
      }
    );

    res.json({
      message: "Login successful",
      token,
      user: {
        id: user._id,
        name: user.name,
        location: user.location,
        phone: user.phone,
        email: user.email,
        role: user.role,
        crop: user.crop,
        price: user.price,
        availability: user.availability
      }
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      message: "Login failed"
    });
  }
});

// GET LOGGED-IN USER PROFILE
app.get("/api/profile", authenticateToken, async (req, res) => {
  try {
    const user = await User.findById(req.user.id)
      .select("-password");

    if (!user) {
      return res.status(404).json({
        message: "User not found"
      });
    }

    res.json(user);
  } catch (error) {
    res.status(500).json({
      message: "Unable to get profile"
    });
  }
});

// UPDATE PROFILE
app.put("/api/profile", authenticateToken, async (req, res) => {
  try {
    const {
      name,
      location,
      phone,
      crop,
      price,
      availability
    } = req.body;

    const updates = {};

    if (name !== undefined) updates.name = name;
    if (location !== undefined) updates.location = location;
    if (phone !== undefined) updates.phone = phone;

    if (req.user.role === "farmer" ||
        req.user.role === "buyer") {
      if (crop !== undefined) updates.crop = crop;
    }

    if (req.user.role === "buyer" &&
        price !== undefined) {
      updates.price = Number(price);
    }

    if (req.user.role === "worker" &&
        availability !== undefined) {
      updates.availability = availability;
    }

    const user = await User.findByIdAndUpdate(
      req.user.id,
      { $set: updates },
      {
        new: true,
        runValidators: true
      }
    ).select("-password");

    res.json({
      message: "Profile updated successfully",
      user
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      message: "Profile update failed"
    });
  }
});

// SEARCH BUYERS BY CROP AND LOCATION
app.get("/api/buyers", async (req, res) => {
  try {
    const { crop, location } = req.query;

    const filter = {
      role: "buyer"
    };

    if (crop) {
      filter.crop = {
        $regex: crop,
        $options: "i"
      };
    }

    if (location) {
      filter.location = {
        $regex: location,
        $options: "i"
      };
    }

    const buyers = await User.find(filter)
      .select("name location phone crop price email");

    res.json(buyers);
  } catch (error) {
    res.status(500).json({
      message: "Unable to search buyers"
    });
  }
});

// SEARCH WORKERS BY LOCATION
app.get("/api/workers", async (req, res) => {
  try {
    const { location, availability } = req.query;

    const filter = {
      role: "worker"
    };

    if (location) {
      filter.location = {
        $regex: location,
        $options: "i"
      };
    }

    if (availability) {
      filter.availability = {
        $regex: availability,
        $options: "i"
      };
    }

    const workers = await User.find(filter)
      .select("name location phone availability email");

    res.json(workers);
  } catch (error) {
    res.status(500).json({
      message: "Unable to search workers"
    });
  }
});

// SEARCH FARMERS
app.get("/api/farmers", async (req, res) => {
  try {
    const { crop, location } = req.query;

    const filter = {
      role: "farmer"
    };

    if (crop) {
      filter.crop = {
        $regex: crop,
        $options: "i"
      };
    }

    if (location) {
      filter.location = {
        $regex: location,
        $options: "i"
      };
    }

    const farmers = await User.find(filter)
      .select("name location phone crop email");

    res.json(farmers);
  } catch (error) {
    res.status(500).json({
      message: "Unable to search farmers"
    });
  }
});

// CONNECT TO MONGODB AND START SERVER
mongoose
  .connect(process.env.MONGODB_URI)
  .then(() => {
    console.log("MongoDB connected successfully");

    app.listen(PORT, "0.0.0.0", () => {
      console.log(`AgriNexa server running on port ${PORT}`);
    });
  })
  .catch((error) => {
    console.error("MongoDB connection failed:", error.message);
  });